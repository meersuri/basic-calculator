exit_code=$(yapf . -r)
if [ exit_code ]
then
    echo "Fail"
else
    echo "Pass"
fi
