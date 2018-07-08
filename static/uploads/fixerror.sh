#!/bin/bash
#fix error in the process of install oracle

ORACLE_HOME=/oracle/app/product/11.2.0/dbhome_1

menu(){
    cat << EOF
Please select number of the error message:
    1.Error in invoking target "install" of makefile：ins_ctx.mk
    2.Error in invoking target 'agent_nmhs' of makefile
    3.Error in invoking target 'all_no_orcl' of makefile
EOF
}

errormessage(){
while true
do
    echo "------------"
    echo  "$1"
    CHOICE=$2
    read NUMBERCHOICE
    Regex_num="^([1-3])$"
    echo $NUMBERCHOICE|grep -E $Regex_num > /dev/null 2>&1
    [ $? -eq 0 ] && eval $CHOICE=$NUMBERCHOICE && break
    [ $? -ne 0 ] && echo -e "Input wrong,please input again: \n"
done
}

menu
errormessage "Please input your choice:" NUMBER

case $NUMBER in
    1)
	bash ins_ctx.sh
	;;
    2)
	sed -i 's/^\(\s*\$(MK_EMAGENT_NMECTL)\)\s*$/\1 -lnnz11/g' $ORACLE_HOME/sysman/lib/ins_emagent.mk
	;;
    3)
	sed -i 's/^\(TNSLSNR_LINKLINE.*\$(TNSLSNR_OFILES)\) \(\$(LINKTTLIBS)\)/\1 -Wl,--no-as-needed \2/g' $ORACLE_HOME/network/lib/env_network.mk
	sed -i 's/^\(ORACLE_LINKLINE.*\$(ORACLE_LINKER)\) \(\$(PL_FLAGS)\)/\1 -Wl,--no-as-needed \2/g' $ORACLE_HOME/rdbms/lib/env_rdbms.mk
	sed -i 's/^\(\$LD \$LD_RUNTIME\) \(\$LD_OPT\)/\1 -Wl,--no-as-needed \2/g' $ORACLE_HOME/bin/genorasdksh
	sed -i 's/^\(\s*\)\(\$(OCRLIBS_DEFAULT)\)/\1 -Wl,--no-as-needed \2/g' $ORACLE_HOME/srvm/lib/ins_srvm.mk
	;;
    *)
	echo "run it again"
esac
