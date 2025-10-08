/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    can.h
  * @brief   This file contains all the function prototypes for
  *          the can.c file
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __CAN_H__
#define __CAN_H__

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* USER CODE BEGIN Includes */


/* USER CODE END Includes */

extern CAN_HandleTypeDef hcan;

/* USER CODE BEGIN Private defines */

#define TRANSMIT_DATA_LENGTH 2 //Sending just pin number for now e.g. "8"
#define TRANSMIT_MSG_ID_VCC  0x580 //VCC ID
#define TRANSMIT_MSG_ID_GND  0x581 //GND ID
#define TRANSMIT_MSG_ID_GPIO  0x582 //GPIO ID
#define CAN_RX_ID 0x103 //Accepted CAN ID
#define CAN_RX_ID2 0x104
#define CAN_RX_ID3 0X105 //IDs for CAN Filter
#define CAN_RX_ID4 0x106

/* USER CODE END Private defines */

void MX_CAN_Init(void);

/* USER CODE BEGIN Prototypes */
void CAN_tx_transmit_msg(uint8_t GPIO_pin,uint8_t port, int mode);
void CAN_filter_init(CAN_FilterTypeDef* can_filter);

/* USER CODE END Prototypes */

#ifdef __cplusplus
}
#endif

#endif /* __CAN_H__ */

