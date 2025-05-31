# Comparison of Empirical and Deep Learning Models for Solar Wind Speed Prediction
This study is a comparison of empirical models (WSA-ENLIL, ESWF 3.2) and deep learning model (Son et al., 2023) for solar wind speed prediction at 1 AU.


## Abstract
In this study, we compare representative empirical models with a deep learning model Son et al. (2023) for predicting solar wind speed at 1 AU. The empirical models are the Wang–Sheeley–Arge (WSA)–ENLIL model, which combines empirical methods with a magnetohydrodynamic model, and the empirical solar wind forecast (ESWF) model, which uses the relationship between the fractional coronal hole area and solar wind speed. Our deep learning model predicts solar wind speed over 3 days ahead using extreme–ultraviolet (EUV) images and up to 5 days of solar wind speed before the prediction date. We evaluate the models over the test period (October–December, 2012–2020) in view of solar activity phases and the entire period. To validate the model's performance, we use two evaluation methods: a statistical approach and an event–based approach. For statistical verification during the entire period, our model outperforms the other empirical models, with a much lower mean absolute error (MAE) of 51.4 km/s and root mean squared error (RMSE) of 68.6 km/s, along with a much higher correlation coefficient (CC) of 0.69. For the event–based verification for high–speed solar wind streams (HSS), our model has superior performance in most of the six metrics evaluated within a ±1–day time window. In particular, it achieves a high success ratio of 0.82, emphasizing the model's stable performance and ability to minimize false alarms. These results show that our deep learning model has strong potential for practical application as a reliable tool of fast solar wind forecasting with its high accuracy and stability. 


## Result 
<img src="https://github.com/user-attachments/assets/b04a6559-4397-4371-98ba-5fc0e885d691" alt="image1" width="800"/>

Solar wind speed at 1 AU during the period of October–December for the years 2012–2020 by OMNI (black), Ours (red), WSA–ENLIL (skyblue), and ESWF 3.2 (green).

### Solar sunspot number vs CC of models
<img src="https://github.com/user-attachments/assets/3c12d951-3785-42db-b17e-4430514ace90" alt="image2" width="800"/>

Variations in the solar sunspot number and the DL model’s CC over the entire period (2012-2020).

### Taylor diagram 
<img src="https://github.com/user-attachments/assets/ab08f67d-f10c-4fef-926a-aff741b8c5ea" alt="image3" width="800"/>

Taylor diagram showing the statistical comparison of RMSE, CC, and standard deviation for solar wind speed prediction models for different solar activity phases and over the entire period.

