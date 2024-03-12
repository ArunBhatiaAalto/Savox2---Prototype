while [ true ]
do
    b1=$(cat /sys/class/gpio/gpio17/value)
    b2=$(cat /sys/class/gpio/gpio27/value)
    b3=$(cat /sys/class/gpio/gpio22/value)

    spi_running=false
    a_running=false

    if [ $b1 == 1 ]
    then
        if [ spi_running ]
        then
	    echo "stop spi"
            killall chwspi
            spi_running=false
        else
	    echo "start spi"
            /home/pi/intelligent-audio-listener/chwspi/chwspi &
            spi_running=true
        fi
    fi

    if [ $b2 == 1 ]
    then
        if [ a_running ]
        then
	    echo "stop main"
            killall main.py
            a_running=false
        else
	    echo "start main"
            /home/pi/intelligent-audio-listener/Main/main.py &
            a_running=true
        fi
    fi

    if [ $b3 == 1 ]
    then
        reboot
    fi

    sleep 0.5

done
