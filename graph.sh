#!/bin/bash

RRA="0"
MIN_WIDTH=1000
HEIGHT=800
LINE_WIDTH=1
DB="/var/log/cirrus-rrd/power"

OPTS="hv:d:o:t:s:e:r:h:w"
LONGOPTS="help,verbose:,database:,output:,start:,end:,rra:,height:,min-width:"
print_help() {
	cat <<EOF
Usage: $(basename $0) [OTHER OPTIONS]

  -h, --help            this help message
  -v, --verbose         show raw data on stdout
  -d, --database        base filename for the .rrd file
  -o, --output          base filename for the .png file
  -t, --type            all, net or system in graph
  -s, --start           start time of graph (defaults to start of archive)
  -e, --end             end time of graph (defaults to end of archive)
  -r, --rra             rra index to use for first and last element   
      --height          graph height (in pixels, default: 800)
      --min-width       minimum graph width (default: 1000)
EOF
}

! PARSED=$(getopt --options=${OPTS} --longoptions=${LONGOPTS} --name "$0" -- "$@")
if [ ${PIPESTATUS[0]} != 0 ]; then
    # getopt has complained about wrong arguments to stdout
    exit 1
fi
# read getopt's output this way to handle the quoting right
eval set -- "$PARSED"

while true; do
	case "$1" in
		-h|--help)
			print_help
			exit
			;;
		-v|--verbose)
			VERBOSE=1
			shift
			;;
		-d|--database)
			DB="$2"
			shift 2
			;;
		-o|--output)
			OUT="$2"
			shift 2
			;;
		-t|--type)
			TYPE="$2"
			shift 2
			;;
		-t|--time)
			TIME="$2"
			shift 2
			;;
		-s|--start)
			START="$2"
			shift 2
			;;
		-e|--end)
			END="$2"
			shift 2
			;;
		-r|--rra)
			RRA="$2"
			shift 2
			;;
		--height)
			HEIGHT="$2"
			shift 2
			;;
		--min-width)
			MIN_WIDTH="$2"
			shift 2
			;;
		--)
			shift
			break
			;;
		*)
			echo "argument parsing error"
			exit 1
	esac
done


COLORS=(
	"#FF0000"
	"#00FF00"
	"#0000FF"
	"#FFF700"
	"#EF843C"
	"#1F78C1"
	"#A05DA0"
    "#A01DA0"
)

if [[ -v START ]]
then
    echo "Start graph at command line argument ${START}"
else
    START="$(rrdtool first --rraindex ${RRA} ${DB}.rrd)"
    echo "Start graph at start of archive ${START}"
fi
if [[ -v END ]]
then
    echo "Finish graph at command line argument ${END}"
else
    END="$(rrdtool last ${DB}.rrd)"
    echo "Finish graph at end of archive ${END}"
fi

NOW=`date +%s`
if [[ ! START =~ [N] ]]
then
    START=$(bc -l <<< ${START/N/$NOW})
fi
if [[ ! END =~ [N] ]]
then
    END=$(bc -l <<< ${END/N/$NOW})
fi

LSTART=`date +%F\ %T -d @$START`
LEND=`date +%F\ %T -d @$END`


rrdtool graph \
    voltage.png \
    --title "Voltage from $LSTART to $LEND" \
    --watermark "$(date)" \
    --slope-mode \
    --alt-y-grid \
    --rigid \
    --start ${START} --end ${END} \
    --width ${MIN_WIDTH} \
    --height ${HEIGHT} \
    --color CANVAS#181B1F \
    --color BACK#111217 \
    --color FONT#CCCCDC \
    DEF:PortA_V=${DB}.rrd:PortA_V:AVERAGE \
        LINE1:PortA_V${COLORS[0]}:"PortA_V\t" \
        GPRINT:PortA_V:AVERAGE:"\t%.2lf" \
        COMMENT:"\n" \
    DEF:PortB_V=${DB}.rrd:PortB_V:AVERAGE \
        LINE1:PortB_V${COLORS[0]}:"PortB_V\t" \
        GPRINT:PortB_V:AVERAGE:"\t%.2lf" \
        COMMENT:"\n" \
    DEF:SPI1_V=${DB}.rrd:SPI1_V:AVERAGE \
        LINE1:SPI1_V${COLORS[0]}:"SPI1_V\t" \
        GPRINT:SPI1_V:AVERAGE:"\t%.2lf" \
        COMMENT:"\n" \
    DEF:SPI2_V=${DB}.rrd:SPI2_V:AVERAGE \
        LINE1:SPI2_V${COLORS[0]}:"SPI2_V\t" \
        GPRINT:SPI2_V:AVERAGE:"\t%.2lf" \
        COMMENT:"\n" \

rrdtool graph \
    current.png \
    --title "Current from $LSTART to $LEND" \
    --watermark "$(date)" \
    --slope-mode \
    --alt-y-grid \
    --rigid \
    --start ${START} --end ${END} \
    --width ${MIN_WIDTH} \
    --height ${HEIGHT} \
    --color CANVAS#181B1F \
    --color BACK#111217 \
    --color FONT#CCCCDC \
    DEF:PortA_I=${DB}.rrd:PortA_I:AVERAGE \
        LINE1:PortA_I${COLORS[0]}:"PortA_I\t" \
        GPRINT:PortA_I:AVERAGE:"\t%.2lf" \
        COMMENT:"\n" \
    DEF:PortB_I=${DB}.rrd:PortB_I:AVERAGE \
        LINE1:PortB_I${COLORS[0]}:"PortB_I\t" \
        GPRINT:PortB_I:AVERAGE:"\t%.2lf" \
        COMMENT:"\n" \
    DEF:SPI1_I=${DB}.rrd:SPI1_I:AVERAGE \
        LINE1:SPI1_I${COLORS[0]}:"SPI1_I\t" \
        GPRINT:SPI1_I:AVERAGE:"\t%.2lf" \
        COMMENT:"\n" \
    DEF:SPI2_I=${DB}.rrd:SPI2_I:AVERAGE \
        LINE1:SPI2_I${COLORS[0]}:"SPI2_I\t" \
        GPRINT:SPI2_I:AVERAGE:"\t%.2lf" \
        COMMENT:"\n" \

rrdtool graph \
    powerfactor.png \
    --title "Power factor from $LSTART to $LEND" \
    --watermark "$(date)" \
    --slope-mode \
    --alt-y-grid \
    --rigid \
    --start ${START} --end ${END} \
    --width ${MIN_WIDTH} \
    --height ${HEIGHT} \
    --color CANVAS#181B1F \
    --color BACK#111217 \
    --color FONT#CCCCDC \
    DEF:PortA_PF=${DB}.rrd:PortA_PF:AVERAGE \
        LINE1:PortA_PF${COLORS[0]}:"PortA_PF\t" \
        GPRINT:PortA_PF:AVERAGE:"\t%.2lf" \
        COMMENT:"\n" \
    DEF:PortB_PF=${DB}.rrd:PortB_PF:AVERAGE \
        LINE1:PortB_PF${COLORS[0]}:"PortB_PF\t" \
        GPRINT:PortB_PF:AVERAGE:"\t%.2lf" \
        COMMENT:"\n" \
    DEF:SPI1_PF=${DB}.rrd:SPI1_PF:AVERAGE \
        LINE1:SPI1_PF${COLORS[0]}:"SPI1_PF\t" \
        GPRINT:SPI1_PF:AVERAGE:"\t%.2lf" \
        COMMENT:"\n" \
    DEF:SPI2_PF=${DB}.rrd:SPI2_PF:AVERAGE \
        LINE1:SPI2_PF${COLORS[0]}:"SPI2_PF\t" \
        GPRINT:SPI2_PF:AVERAGE:"\t%.2lf" \
        COMMENT:"\n" \
