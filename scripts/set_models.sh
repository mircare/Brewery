#!/bin/bash

# Brewery: prediction of 1D protein structure annotations (https://github.com/mircare/Brewery)
# Email us at gianluca[dot]pollastri[at]ucd[dot]ie if you wish to use it for purposes not permitted by the CC BY-NC-SA 4.0.

# set absolute paths for all model files required by Brewery

# SS3
echo `ls Predict_BRNN/models/SS3/*v7|wc -w` > Predict_BRNN/models/modelv7_ss3
ls Predict_BRNN/models/SS3/*v7 >> Predict_BRNN/models/modelv7_ss3
echo `ls Predict_BRNN/models/SS3/*v8|wc -w` > Predict_BRNN/models/modelv8_ss3
ls Predict_BRNN/models/SS3/*v8 >> Predict_BRNN/models/modelv8_ss3
echo `ls Predict_BRNN/models/SS3/*v78|wc -w` > Predict_BRNN/models/modelv78_ss3
ls Predict_BRNN/models/SS3/*v78 >> Predict_BRNN/models/modelv78_ss3
echo `ls Predict_BRNN/models/SS3/*v8_BFD|wc -w` > Predict_BRNN/models/modelv8_BFD_ss3
ls Predict_BRNN/models/SS3/*v8_BFD >> Predict_BRNN/models/modelv8_BFD_ss3
echo `ls Predict_BRNN/models/SS3/*v8_HH+BFD|wc -w` > Predict_BRNN/models/modelv8_HH+BFD_ss3
ls Predict_BRNN/models/SS3/*v8_HH+BFD >> Predict_BRNN/models/modelv8_HH+BFD_ss3

# SS8
echo `ls Predict_BRNN/models/SS8/*PSI3* |wc -w` > Predict_BRNN/models/modelv7_ss8
ls Predict_BRNN/models/SS8/*PSI3* >> Predict_BRNN/models/modelv7_ss8
echo `ls Predict_BRNN/models/SS8/*HH3* |wc -w` > Predict_BRNN/models/modelv8_ss8
ls Predict_BRNN/models/SS8/*HH3* >> Predict_BRNN/models/modelv8_ss8
echo `ls Predict_BRNN/models/SS8/*HHpsi* |wc -w` > Predict_BRNN/models/modelv78_ss8
ls Predict_BRNN/models/SS8/*HHpsi3* >> Predict_BRNN/models/modelv78_ss8
echo `ls Predict_BRNN/models/SS8/*_BFD|wc -w` > Predict_BRNN/models/modelv8_BFD_ss8
ls Predict_BRNN/models/SS8/*_BFD >> Predict_BRNN/models/modelv8_BFD_ss8
echo `ls Predict_BRNN/models/SS8/*_HH+BFD|wc -w` > Predict_BRNN/models/modelv8_HH+BFD_ss8
ls Predict_BRNN/models/SS8/*_HH+BFD >> Predict_BRNN/models/modelv8_HH+BFD_ss8

# TA14
echo `ls Predict_BRNN/models/TA14/*v7 |wc -w` > Predict_BRNN/models/modelv7_ta14
ls Predict_BRNN/models/TA14/*v7 >> Predict_BRNN/models/modelv7_ta14
echo `ls Predict_BRNN/models/TA14/*v8 |wc -w` > Predict_BRNN/models/modelv8_ta14
ls Predict_BRNN/models/TA14/*v8 >> Predict_BRNN/models/modelv8_ta14
echo `ls Predict_BRNN/models/TA14/*v78 |wc -w` > Predict_BRNN/models/modelv78_ta14
ls Predict_BRNN/models/TA14/*v78 >> Predict_BRNN/models/modelv78_ta14
echo `ls Predict_BRNN/models/TA14/*_BFD |wc -w` > Predict_BRNN/models/modelv8_BFD_ta14
ls Predict_BRNN/models/TA14/*_BFD >> Predict_BRNN/models/modelv8_BFD_ta14
echo `ls Predict_BRNN/models/TA14/*_HH+BFD |wc -w` > Predict_BRNN/models/modelv8_HH+BFD_ta14
ls Predict_BRNN/models/TA14/*_HH+BFD >> Predict_BRNN/models/modelv8_HH+BFD_ta14

# SA4
echo `ls Predict_BRNN/models/SA4/*v7 |wc -w` > Predict_BRNN/models/modelv7_sa4
ls Predict_BRNN/models/SA4/*v7 >> Predict_BRNN/models/modelv7_sa4
echo `ls Predict_BRNN/models/SA4/*v8 |wc -w` > Predict_BRNN/models/modelv8_sa4
ls Predict_BRNN/models/SA4/*v8 >> Predict_BRNN/models/modelv8_sa4
echo `ls Predict_BRNN/models/SA4/*v78 |wc -w` > Predict_BRNN/models/modelv78_sa4
ls Predict_BRNN/models/SA4/*v78 >> Predict_BRNN/models/modelv78_sa4
echo `ls Predict_BRNN/models/SA4/*_BFD |wc -w` > Predict_BRNN/models/modelv8_BFD_sa4
ls Predict_BRNN/models/SA4/*_BFD >> Predict_BRNN/models/modelv8_BFD_sa4
echo `ls Predict_BRNN/models/SA14/*_HH+BFD |wc -w` > Predict_BRNN/models/modelv8_HH+BFD_sa4
ls Predict_BRNN/models/SA4/*_HH+BFD >> Predict_BRNN/models/modelv8_HH+BFD_sa4

# CD4
echo `ls Predict_BRNN/models/CD4/*v7 |wc -w` > Predict_BRNN/models/modelv7_cd4
ls Predict_BRNN/models/CD4/*v7 >> Predict_BRNN/models/modelv7_cd4
echo `ls Predict_BRNN/models/CD4/*v8 |wc -w` > Predict_BRNN/models/modelv8_cd4
ls Predict_BRNN/models/CD4/*v8 >> Predict_BRNN/models/modelv8_cd4
echo `ls Predict_BRNN/models/CD4/*v78 |wc -w` > Predict_BRNN/models/modelv78_cd4
ls Predict_BRNN/models/CD4/*v78 >> Predict_BRNN/models/modelv78_cd4
echo `ls Predict_BRNN/models/CD4/*_BFD |wc -w` > Predict_BRNN/models/modelv8_BFD_cd4
ls Predict_BRNN/models/CD4/*_BFD >> Predict_BRNN/models/modelv8_BFD_cd4
echo `ls Predict_BRNN/models/CD4/*_HH+BFD |wc -w` > Predict_BRNN/models/modelv8_HH+BFD_cd4
ls Predict_BRNN/models/CD4/*_HH+BFD >> Predict_BRNN/models/modelv8_HH+BFD_cd4

abs_path=`pwd`
sed -i'' -e "s|Predict_BRNN/models|$abs_path\/Predict_BRNN/models|g" Predict_BRNN/models/modelv*
cd ../../
