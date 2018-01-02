
//
//  Algorithm_team_project.c
//  practice1
//
//  Created by 박성진 on 2017. 11. 16..
//  Copyright © 2017년 박성진. All rights reserved.
//

#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>

#define True 1
#define False 0
#define PORT 11120
#define IP "127.0.0.1"

typedef struct
{
    int input_size;
    int hidden_size;
    int output_size;
    int training_set;
    double learning_rate;
    double delta_weight1[100000];
    double delta_weight2[100000];

    double input_data[100000][100000];
    double output_data[100000][100000];
    double hidden_output[100000];
    double final_output[100000];

    double test_input[100000];
    double test_output[100000];

    double weight1[100000][100000];
    double weight2[100000][100000];
}Model;

void sock_send(int sock_fd, char message[])
{
    write(sock_fd, message, strlen(message));
}

void sock_read(int sock_fd, char message[])
{
    read(sock_fd, message, 99);
}

// 다중 퍼셉트론 모델에서의 활성화 함수.
// 파라미터: x (입력값에 가중치를 곱한 값.). deriv ( 활성화 함수의 미분 값을 출력해준다. )
// 만약 deriv가 거짓이라면 그냥 시그모이드 값을 반환
// 만약 deriv가 참이라면 미분된 시그모이드 함수의 값을 반환한다.
double sigmoid(double x, int deriv)
{
    if(deriv == 1)
    {
        return (1-x)*x;
    }
    return 1/(1 + exp(-x));
}

// 행렬 곱을 위한 함수.
// 파라미터: a (피연산자1), b (피연산자2), size_a (a 행렬의 크기), size_b (b 행렬의 크기)
// 반환값: a * b 결과를 저장한 배 (matrix multiplication)
void mat_mul(double a[], double b[][100000], int size_a, int size_b, double total_result[], int in_hid)
{
    double result = 0;

    if (in_hid) {
        for (int i = 0; i < size_b; i++) {
            result = 0;
            for (int j = 0; j < size_a; j++) {
                if (j == 1)
                {
                    result += 1*b[(int)a[j]][i];
                }else if (j == 2){
                    result += 1*b[(int)a[j]+1][i];
                }else{
                    result += a[j]*b[j][i];
                }
            }
            total_result[i] = sigmoid(result, False);
            //            printf("%lf\n", total_result[i]);
        }
        return;
    }

    for (int i = 0; i < size_b; i++) {
        result = 0;
        for (int j = 0; j < size_a; j++) {
            result += a[j]*b[j][i];
        }
        total_result[i] = sigmoid(result, False);
    }
}

// 은닉층 출력값과 출력층 출력값을 계산한다.
// 파라미터: 입력층에 들어오는 입력값, 은닉층 결과를 저장할 배열, 출력층 결과를 저장할 배열, 입력층-은닉층 사이 가중치, 은닉층-출력층 사이 가중치, 입력층 크기, 은닉층 크기, 출력층 크기
// 반환값: 없음
void forward(double input_data[], Model *model)
{
    mat_mul(input_data, model->weight1, model->input_size, model->hidden_size, model->hidden_output, 1);       // 은닉층의 출력값을 계산한다.
    mat_mul(model->hidden_output, model->weight2, model->hidden_size, model->output_size, model->final_output, 0);    // 출력층의 출력값을 계산한다.
}

// 실제 결과값과 예측 결과값의 차이를 계산한다.
// 파라미터: 실제 결과값, 출력층 결과, 은닉층 결과, 출력층-은닉층 사이의 변화를 저장하는 배열, 은닉층-출력층 사이의 변화를 저장하는 배열, 은닉층-출력층 사이 가중치, 입력층-은닉층 사이 가중치, 입력층 크기, 은닉층 크기, 출력층 크기
// 반환값: 없음
double back_propagation(double output_data[], Model *model)
{
    double delta = 0;
    double error = 0;
    for (int i = 0; i < model->output_size; i++) {                         // 출력층의 출력값과 실제 결과값의 차이를 계산한다.
        delta = output_data[i] - model->final_output[i];
        model->delta_weight2[i] = delta * sigmoid(model->final_output[i], True);
    }

    for (int i = 0; i < model->hidden_size; i++) {                         // 은닉층의 결과가 예측 결과값과 실제 결과값의 차이에 얼마나 영향을 주는지 계산한다.
        delta = 0;
        for (int j = 0; j < model->output_size; j++) {
            delta += model->delta_weight2[j] * model->weight2[i][j];
        }
        model->delta_weight1[i] = delta * sigmoid(model->hidden_output[i], True);
    }

    error = 0;
    for (int i = 0; i < model->output_size; i++) {
        error += pow((output_data[i] - model->final_output[i]), 2);
    }
    error = sqrt(error/model->output_size);
    return error;
}

// 위에서 계산한 delta값을 이용해 가중치를 변경한다.
// 파라미터: 입력층에 들어오는 입력값, 은닉층 결과값, 출력층-은닉층 사이의 변화를 저장하는 배열, 은닉층-출력층 사이의 변화를 저장하는 배열, 은닉층-출력층 사이 가중치, 입력층-은닉층 사이 가중치, 입력층 크기, 은닉층 크기, 출력층 크기, 학습률
// 반환값: 없음
void training(double input_data[], Model *model)
{
    double change = 0;

    for (int i = 0; i < model->hidden_size; i++) {                                         // 출력층과 은닉층 사이의 가중치를 조절한다.
        for (int j = 0; j < model->output_size; j++) {
            change = model->delta_weight2[j] * model->hidden_output[i];
            model->weight2[i][j] += model->learning_rate * change;
        }
    }

    for (int i = 0; i < model->input_size; i++) {                                          // 입력층과 은닉층 사이의 가중치를 조절한다.
        for (int j = 0; j < model->hidden_size; j++) {
            if (i == 1)
            {
                change = model->delta_weight1[j] * 1;
                model->weight1[(int)input_data[i]][j] += model->learning_rate * change;
            }else if(i == 2){
                change = model->delta_weight1[j] * 1;
                model->weight1[(int)input_data[i]+1][j] += model->learning_rate * change;
            }else{
                change = model->delta_weight1[j] * input_data[i];
                model->weight1[i][j] += model->learning_rate * change;
            }
        }
    }

    // 변화량을 초기화한다.
    for (int i = 0; i < model->hidden_size; i++) {
        model->delta_weight1[i] = 0;
    }
    for (int i = 0; i < model->output_size; i++) {
        model->delta_weight2[i] = 0;
    }
}

void test(double input_data[], Model *model, double result[])
{
    mat_mul(input_data, model->weight1, model->input_size, model->hidden_size, model->hidden_output, 1);       // 은닉층의 출력값을 계산한다.
    mat_mul(model->hidden_output, model->weight2, model->hidden_size, model->output_size, result, 0);    // 출력층의 출력값을 계산한다.
}

int main(void)
{
    double test_input[500] = {1, 0};
    double test_output[100] = {0};
    double real_output[100] = {0};
    double error_rate = 0;
    int idx = 0;
    double correct = 0.0;
    int line = 0;
    int station_code = 0;
    int hour = 0;
    int minute = 0;
    char write_buf[100] = {0};
    char read_buf[100] = {0};

    int sockfd = 0, n = 0;
    char recvBuff[1024];
    struct sockaddr_in serv_addr;
    memset(recvBuff, '0',sizeof(recvBuff));

    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Error : Could not create socket \n");
        return 1;
    }
    memset(&serv_addr, '0', sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    if(inet_pton(AF_INET, IP, &serv_addr.sin_addr)<=0)
    {
        printf("\n inet_pton error occured\n");
        return 1;
    }

    if( connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\n Error : Connect Failed \n");
        return 1;
    }

    sock_send(sockfd, write_buf);

    FILE *fp_in = fopen("/Users/Knight/Desktop/input.csv", "r");
    FILE *fp_out = fopen("/Users/Knight/Desktop/output.csv", "r");

    Model *model = malloc(sizeof(Model));

    srand(time(NULL));

    model->input_size = 3;
    model->hidden_size = 3;
    model->output_size = 1;
    model->training_set = 19992;
    model->learning_rate = 0.1;

    while (1) {
        for (int i=0; i < 3; i ++) {
            fscanf(fp_in, "%lf", &(model->input_data[idx][i]));
        }
        if (feof(fp_in)) {
            break;
        }
        idx += 1;
    }
    idx = 0;

    while (1) {
        fscanf(fp_out, "%lf", &(model->output_data[idx][0]));
        if (feof(fp_out)) {
            break;
        }
        idx += 1;
    }

    fclose(fp_in);
    fclose(fp_out);

    for (int i = 0; i < 1; i++) {
        for (int j = 0; j < 1; j++) {
            model->weight1[i][j] = (double)rand()/(double)RAND_MAX;
            model->weight2[i][j] = (double)rand()/(double)RAND_MAX;
        }
    }

    for (int z = 0; z < 100; z++) {
        error_rate = 0;
        if (z%10 == 0) {
            idx = 0;
            correct = 0;
            fp_in = fopen("/Users/Knight/Desktop/test_input.csv", "r");
            fp_out = fopen("/Users/Knight/Desktop/test_output.csv", "r");
            while (1) {
                idx += 1;
                for (int i=0; i < 3; i ++) {
                    fscanf(fp_in, "%lf", &test_input[i]);
                }
                fscanf(fp_out, "%lf", &real_output[0]);
                test(test_input, model, test_output);
                if (round(test_output[0]) == real_output[0]) {
                    correct += 1;
                }
                if (feof(fp_in)) {
                    break;
                }
            }
        }

        for (int i = 0; i < model->training_set; i++) {
            forward(model->input_data[i], model);
            error_rate += back_propagation(model->output_data[i], model);
            training(model->input_data[i], model);
        }

        if (z%10 == 0) {
            snprintf(write_buf, 100, "%lf %lf\n",correct/idx, error_rate/model->training_set);
            sock_send(sockfd, write_buf);
            fclose(fp_in);
            fclose(fp_out);
        }
//        printf("%lf\n", error_rate);
    }

    printf("Training finished, Testing start\n");
    idx = 0;
    correct = 0;
    fp_in = fopen("/Users/Knight/Desktop/test_input.csv", "r");
    fp_out = fopen("/Users/Knight/Desktop/test_output.csv", "r");
    while (1) {
        idx += 1;
        for (int i=0; i < 3; i ++) {
            fscanf(fp_in, "%lf", &test_input[i]);
        }
        fscanf(fp_out, "%lf", &real_output[0]);
        test(test_input, model, test_output);
        if (round(test_output[0]) == real_output[0]) {
            correct += 1;
        }
        if (feof(fp_in)) {
            break;
        }
    }

    printf("Total test case: %d, Correct test case: %d, correction_rate: %lf\n", idx, (int)correct, correct/idx);
    snprintf(write_buf, 100, "Total test case: %d, Correct test case: %d, correction_rate: %lf\n", idx, (int)correct, correct/idx);
    sock_send(sockfd, write_buf);

    fclose(fp_in);
    fclose(fp_out);

    printf("Type Line #, Station code, Time(hh:mm)\n");
    snprintf(write_buf, 100, "Type Line #, Station code, Time(hh:mm)\n");
    sock_send(sockfd, write_buf);

    while (1) {

        sock_read(sockfd, read_buf);
        sscanf(read_buf, "%d %d %d:%d", &line, &station_code, &hour, &minute);
        printf("%s\n", read_buf);
        test_input[0] = (double)line;
        test_input[1] = (double)station_code;
        test_input[2] = (double)hour;
        test(test_input, model, test_output);
        if (test_output[0] > 0.5) {
            printf("Busy\n");
            snprintf(write_buf, 100, "Busy\n");
        }else{
            printf("Not busy\n");
            snprintf(write_buf, 100, "Not busy\n");
        }

        memset(read_buf, 0, 100);
        sock_send(sockfd, write_buf);
    }
}
