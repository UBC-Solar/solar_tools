/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
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
#include "main.h"
#include "can.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
typedef struct {
    GPIO_TypeDef *port;
    uint16_t pin;
    char *name;   // optional, for debug prints
} PinConfig;


typedef struct {
    GPIO_TypeDef *port;
    uint16_t pin;
    char *name;   // optional, for debug prints
    int mode; //0 for reading 1 for writing
} PinConfig_full;
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */


PinConfig pins_to_check_[] = {
    {GPIOC, GPIO_PIN_13, "PC13"},
    {GPIOA, GPIO_PIN_4,  "PA4"},
    {GPIOA, GPIO_PIN_0,  "PA0"},
	{GPIOC, GPIO_PIN_3,  "PC3"},
    {GPIOA, GPIO_PIN_3,  "PA3"},
    {GPIOB, GPIO_PIN_11, "PB11"},
    {GPIOA, GPIO_PIN_13, "PA13"},
    {GPIOB, GPIO_PIN_9,  "PB9"}

};

PinConfig_full pins_full[] = {
    {GPIOC, GPIO_PIN_13, "PC13", 0},
    {GPIOC, GPIO_PIN_14, "PC14", 1},
    {GPIOC, GPIO_PIN_15, "PC15", 0},
    {GPIOD, GPIO_PIN_0,  "PD0",  1},
    {GPIOD, GPIO_PIN_1,  "PD1",  0},
    {GPIOC, GPIO_PIN_0,  "PC0",  1},
    {GPIOC, GPIO_PIN_1,  "PC1",  0},
    {GPIOC, GPIO_PIN_2,  "PC2",  1},
    {GPIOC, GPIO_PIN_3,  "PC3",  0},
    {GPIOA, GPIO_PIN_0,  "PA0",  0},
    {GPIOA, GPIO_PIN_1,  "PA1",  1},
    {GPIOA, GPIO_PIN_2,  "PA2",  0},
    {GPIOA, GPIO_PIN_3,  "PA3",  0},
    {GPIOA, GPIO_PIN_4,  "PA4",  0},
    {GPIOA, GPIO_PIN_5,  "PA5",  0},
    {GPIOA, GPIO_PIN_6,  "PA6",  1},
    {GPIOA, GPIO_PIN_7,  "PA7",  1},
    {GPIOC, GPIO_PIN_4,  "PC4",  0},
    {GPIOC, GPIO_PIN_5,  "PC5",  0},
    {GPIOB, GPIO_PIN_0,  "PB0",  1},
    {GPIOB, GPIO_PIN_1,  "PB1",  1},
    {GPIOB, GPIO_PIN_2,  "PB2",  1},
    {GPIOB, GPIO_PIN_10, "PB10", 1},
    {GPIOB, GPIO_PIN_11, "PB11", 1},
    {GPIOB, GPIO_PIN_12, "PB12", 1},
    {GPIOB, GPIO_PIN_13, "PB13", 0},
    {GPIOB, GPIO_PIN_14, "PB14", 1},
    {GPIOB, GPIO_PIN_15, "PB15", 0},
    {GPIOC, GPIO_PIN_6,  "PC6",  1},
    {GPIOC, GPIO_PIN_7,  "PC7",  0},
    {GPIOC, GPIO_PIN_8,  "PC8",  1},
    {GPIOC, GPIO_PIN_9,  "PC9",  0},
    {GPIOA, GPIO_PIN_8,  "PA8",  1},
    {GPIOA, GPIO_PIN_9,  "PA9",  0},
    {GPIOA, GPIO_PIN_10, "PA10", 1},
    {GPIOA, GPIO_PIN_11, "PA11", 0},
    {GPIOA, GPIO_PIN_12, "PA12", 1},
    {GPIOA, GPIO_PIN_13, "PA13", 0},
    {GPIOA, GPIO_PIN_14, "PA14", 0},
    {GPIOA, GPIO_PIN_15, "PA15", 0},
    {GPIOC, GPIO_PIN_10, "PC10", 0},
    {GPIOC, GPIO_PIN_11, "PC11", 0},
    {GPIOC, GPIO_PIN_12, "PC12", 0},
    {GPIOD, GPIO_PIN_2,  "PD2",  0},
    {GPIOB, GPIO_PIN_3,  "PB3",  1},
    {GPIOB, GPIO_PIN_4,  "PB4",  1},
    {GPIOB, GPIO_PIN_5,  "PB5",  1},
    {GPIOB, GPIO_PIN_6,  "PB6",  1},
    {GPIOB, GPIO_PIN_7,  "PB7",  1} //Note PB8 and PB9 are not Set to GPIOs since theyre for CAN_TX/RX
};

const int PINS_ALL_COUNT = sizeof(pins_to_check_full) / sizeof(pins_to_check_full[0]);
int MAX_PINS = 64;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *hcan)
{
  if (HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &RxHeader, RxData) != HAL_OK)
  {
    Error_Handler();
  }
  if ((RxHeader.StdId == 0x103))
  {
	  datacheck = 1;
  }
}

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */
	int short_flag = 0;
	int loop = 7;
	int check1 = 2;
	int loop1 = 51;

	TxData[0] = 50;
	TxData[1] = 0xAA;

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_CAN_Init();
  /* USER CODE BEGIN 2 */




  for(int i = 0; i<=loop; i++){
	  uint8_t state = HAL_GPIO_ReadPin(pins_to_check[i].port, pins_to_check[i].pin);
	  if(state == 1 && i <= check1 ) {
		  printf("Pin %s is shorted to VCC\n", pins_to_check[i].name);
		  short_flag = 1;
	  }
	  if(state == 0 && i > check1 ){
		  printf("Pin %s is shorted to GND\n", pins_to_check[i].name);
		  short_flag = 1;
	  }

  }

  if(short_flag == 0){

uint8_t base[MAX_PINS];

	for(int i = 0; i<PINS_ALL_COUNT; i++) {
		if(pins_full[i].mode == 1){
			HAL_GPIO_WritePin(pins_full[i].port, pins_full[i].pin, GPIO_PIN_RESET);
		}

	}

HAL_Delay(1);

	for(int i = 0; i<PINS_ALL_COUNT; i++) {

		base[i] = HAL_GPIO_ReadPin(pins_full[i].port, pins_full[i].pin); //All pins are read to this array

	}


	for (int i = 0; i<PINS_ALL_COUNT; i++) {

		if(pins_full[i].mode == 1) { //If pin is in write mode


			//Outputs High - Checks shorts between pins with Pull-down
			HAL_GPIO_WritePin(pins_full[i].port, pins_full[i].pin, GPIO_PIN_SET);
			HAL_Delay(1);

			for (int j = 0; j<PINS_ALL_COUNT; j++) if( j!= i) {
				uint8_t in_value = HAL_GPIO_ReadPin(pins_full[j].port, pins_full[j].pin);
				if(base[j] == 0 && in_val == 1){ //if statement checks if values being read changed
					printf("Short at %s\n", pins_all[i].name);

				}
			}

			//Outputs Low  - Checks shorts between pins with Pull-up
			HAL_GPIO_WritePin(pins_full[i].port, pins_full[i].pin, GPIO_PIN_RESET);
			HAL_Delay(1);

			for (int j = 0; j<PINS_ALL_COUNT; j++) if( j!= i) {
				uint8_t in_value = HAL_GPIO_ReadPin(pins_full[j].port, pins_full[j].pin);
				if(base[j] == 1 && in_val == 0){ //if statement checks if values being read changed
					printf("Short at %s\n", pins_full[i].name);

				}
			}

		}

	}


  }


  if (HAL_CAN_AddTxMessage(&hcan1, &TxHeader, TxData, &TxMailbox) != HAL_OK) {

  	Error_Handler ();
  }

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */


	  if (datacheck)
	  {
	   Printf("CAN_Message_Read! \n");
	   datacheck = 0;
	  }


	  //Set pins in here, or wait until its set, etc
	  //code doesn't need to be in here, but needs to reach here at the end and see if successful or not


  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}
#ifdef USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
