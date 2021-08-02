#!/bin/zsh

accountid=399183407968

aws glacier list-vaults --account-id $accountid --query 'VaultList[*].VaultName'

v1=arq_0C92BB81-6578-404A-A3F9-F2B6F1B693DA
v2=arq_653043B6-35F3-4771-8741-6AA8501F60EC
jobid1=X2BEAfIKc15wECC9sHpln4sXKNBCmashQmkxOjYWCwyy37AKquuWc_LvaX9prPI5sGLR0eSMo4KMSkGsYGW6gKPj3kRU
jobid2=qI2jHzIx9m7gZP52P4RukQoxBF045rNHtmDdMr3ZcOyhlwT1yrqN3EdUKF80Z16_6s6rvEeEJAGBAMPU-DG1FLXSnGFU

j1=`aws glacier describe-job --vault-name $v1 --account-id $accountid --job-id $jobid1 --query "StatusCode"`
j2=`aws glacier describe-job --vault-name $v2 --account-id $accountid --job-id $jobid2 --query "StatusCode"`

if test $j1 = '"InProgress"'; then
    echo "j1 is $j1"
else
    echo "j1 not InProgress $j1"
    ls -l output1.json
    echo "Now run..."
    echo "python3 delete-archives2.py output1.json"
fi

if test $j2 = '"InProgress"'; then
    echo "j2 is $j2"
else
    echo "j2 not InProgress - $j2"
    ls -l output1.json
    echo "Now run..."
    echo "python3 delete-archives2.py output2.json"
fi


