/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    can.c
  * @brief   This file provides code for the configuration
  *          of the CAN instances.
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
/* Includes ------------------------------------------------------------------*/
#include "can.h"

/* USER CODE BEGIN 0 */

/* Private Includes */


#define TRANSMIT_DATA_LENGTH 2 //Sending just pin number for now e.g. "8"
#define TRANSMIT_MSG_ID_VCC  0x580 //VCC ID
#define TRANSMIT_MSG_ID_GND  0x581 //GND ID
#define TRANSMIT_MSG_ID_GPIO  0x582 //GPIO ID
#define CAN_RX_ID 0x103
#define CAN_RX_ID2 0x104
#define CAN_RX_ID3 0X105
#define CAN_RX_ID4 0x106

CAN_TxHeaderTypeDef transmit_header_VCC = {
    .StdId = TRANSMIT_MSG_ID_VCC,    // your chosen 11-bit ID
    .ExtId = 0x0000,                          // ignored in standard frame
    .IDE   = CAN_ID_STD,                      // standard frame
    .RTR   = CAN_RTR_DATA,                    // data frame, not remote
    .DLC   = TRANSMIT_DATA_LENGTH  // payload length (0-8)
};

CAN_TxHeaderTypeDef transmit_header_GND = {
    .StdId = TRANSMIT_MSG_ID_GND,    // your chosen 11-bit ID
    .ExtId = 0x0000,                          // ignored in standard frame
    .IDE   = CAN_ID_STD,                      // standard frame
    .RTR   = CAN_RTR_DATA,                    // data frame, not remote
    .DLC   = TRANSMIT_DATA_LENGTH  // payload length (0-8)
};

CAN_TxHeaderTypeDef transmit_header_GPIO = {
    .StdId = TRANSMIT_MSG_ID_GPIO,    // your chosen 11-bit ID
    .ExtId = 0x0000,                          // ignored in standard frame
    .IDE   = CAN_ID_STD,                      // standard frame
    .RTR   = CAN_RTR_DATA,                    // data frame, not remote
    .DLC   = TRANSMIT_DATA_LENGTH  // payload length (0-8)
};

CAN_FilterTypeDef can_filter = {0};

/* USER CODE END 0 */

CAN_HandleTypeDef hcan;

/* CAN init function */
void MX_CAN_Init(void)
{

  /* USER CODE BEGIN CAN_Init 0 */

  /* USER CODE END CAN_Init 0 */

  /* USER CODE BEGIN CAN_Init 1 */

  /* USER CODE END CAN_Init 1 */
  hcan.Instance = CAN1;
  hcan.Init.Prescaler = 8;
  hcan.Init.Mode = CAN_MODE_NORMAL;
  hcan.Init.SyncJumpWidth = CAN_SJW_1TQ;
  hcan.Init.TimeSeg1 = CAN_BS1_4TQ;
  hcan.Init.TimeSeg2 = CAN_BS2_4TQ;
  hcan.Init.TimeTriggeredMode = DISABLE;
  hcan.Init.AutoBusOff = ENABLE;
  hcan.Init.AutoWakeUp = DISABLE;
  hcan.Init.AutoRetransmission = ENABLE;
  hcan.Init.ReceiveFifoLocked = DISABLE;
  hcan.Init.TransmitFifoPriority = DISABLE;
  if (HAL_CAN_Init(&hcan) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN CAN_Init 2 */

  CAN_filter_init(&can_filter); //Initializes CAN filter
  HAL_CAN_Start(&hcan);

	  if (HAL_CAN_ActivateNotification(&hcan, CAN_IT_RX_FIFO0_MSG_PENDING) != HAL_OK)
		     {
		   	  Error_Handler();
		     }

  /* USER CODE END CAN_Init 2 */

}

void HAL_CAN_MspInit(CAN_HandleTypeDef* canHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  if(canHandle->Instance==CAN1)
  {
  /* USER CODE BEGIN CAN1_MspInit 0 */

  /* USER CODE END CAN1_MspInit 0 */
    /* CAN1 clock enable */
    __HAL_RCC_CAN1_CLK_ENABLE();

    __HAL_RCC_GPIOB_CLK_ENABLE();
    /**CAN GPIO Configuration
    PB8     ------> CAN_RX
    PB9     ------> CAN_TX
    */
    GPIO_InitStruct.Pin = GPIO_PIN_8;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    GPIO_InitStruct.Pin = GPIO_PIN_9;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    __HAL_AFIO_REMAP_CAN1_2();

    /* CAN1 interrupt Init */
    HAL_NVIC_SetPriority(USB_HP_CAN1_TX_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(USB_HP_CAN1_TX_IRQn);
    HAL_NVIC_SetPriority(USB_LP_CAN1_RX0_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(USB_LP_CAN1_RX0_IRQn);
    HAL_NVIC_SetPriority(CAN1_RX1_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(CAN1_RX1_IRQn);
    HAL_NVIC_SetPriority(CAN1_SCE_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(CAN1_SCE_IRQn);
  /* USER CODE BEGIN CAN1_MspInit 1 */

  /* USER CODE END CAN1_MspInit 1 */
  }
}

void HAL_CAN_MspDeInit(CAN_HandleTypeDef* canHandle)
{

  if(canHandle->Instance==CAN1)
  {
  /* USER CODE BEGIN CAN1_MspDeInit 0 */

  /* USER CODE END CAN1_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_CAN1_CLK_DISABLE();

    /**CAN GPIO Configuration
    PB8     ------> CAN_RX
    PB9     ------> CAN_TX
    */
    HAL_GPIO_DeInit(GPIOB, GPIO_PIN_8|GPIO_PIN_9);

    /* CAN1 interrupt Deinit */
    HAL_NVIC_DisableIRQ(USB_HP_CAN1_TX_IRQn);
    HAL_NVIC_DisableIRQ(USB_LP_CAN1_RX0_IRQn);
    HAL_NVIC_DisableIRQ(CAN1_RX1_IRQn);
    HAL_NVIC_DisableIRQ(CAN1_SCE_IRQn);
  /* USER CODE BEGIN CAN1_MspDeInit 1 */

  /* USER CODE END CAN1_MspDeInit 1 */
  }
}

/* USER CODE BEGIN 1 */
/**
 * @brief CAN message to transmit the pin getting shorted
 */
void CAN_tx_transmit_msg(uint8_t GPIO_pin, uint8_t port, int mode) {


  uint8_t transmit_pin[2];
  transmit_pin[0] = port;
  transmit_pin[1] = GPIO_pin;

  uint32_t mailbox;

  if (mode == 0) {
	  HAL_CAN_AddTxMessage(&hcan, &transmit_header_VCC, transmit_pin, &mailbox);
  }

  if (mode == 1) {
	  HAL_CAN_AddTxMessage(&hcan, &transmit_header_GND, transmit_pin, &mailbox);
  }

  if (mode == 2) {
	  HAL_CAN_AddTxMessage(&hcan, &transmit_header_GPIO, transmit_pin, &mailbox);
  }
}




void CAN_filter_init(CAN_FilterTypeDef* can_filter) {

	//Accepts ID : 0x103, 0x104, 0x105, 0x106

	   can_filter->FilterIdHigh = (CAN_RX_ID << 5);
	   can_filter->FilterMaskIdHigh = (CAN_RX_ID2 << 5);
	   can_filter->FilterIdLow = (CAN_RX_ID3 << 5);
	   can_filter->FilterMaskIdLow = (CAN_RX_ID4 << 5);
	   can_filter->FilterFIFOAssignment = CAN_FILTER_FIFO0;
	   can_filter->FilterBank = 0;
	   can_filter->FilterMode = CAN_FILTERMODE_IDLIST;
	   can_filter->FilterScale = CAN_FILTERSCALE_16BIT;
	   can_filter->FilterActivation = ENABLE;
	   HAL_CAN_ConfigFilter(&hcan, can_filter);


}





/* USER CODE END 1 */
