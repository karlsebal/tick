#!/bin/bash

shopt -s extglob

short_help () {
	echo "usage: ${0##*/} -hadmyDY [command] <time> <description>"
}

help() {
	short_help

	cat <<-EOF

		options:

		-h	help
		
		-d	set day
		-m	set month
		-y	set year
		-D	set date
		-Y	set to yesterday

		Note: -D option is dominant over -dmy. With -Y mixed last given wins.

		-a	set amamedis


		commands:

		parse
		state
		report
		sync

		undo
		redo

		completion

EOF
}

# if an option or bunch of options
# they are parsed into an array
# if option demands an argument 
# its read from $1 and $skip_next is increased
# shifts are done for option, bunch of options
# and parameter demanded by an option

# the stripped commandline
stripped=""
# number of arguments to be skipped
skip_next=0

for arg in "$@"; do

	# skip arguments demanded by options
	# and already shifted
	[[ $skip_next -gt 0 ]] && {
		((skip_next--))
		continue
	}

	# shift for every command, option, bunch
	shift

	# options parsing
	# if we encount an option we will unset arg[0]
	# and move options to $arg[0+n]

	# do we have a bunch of options?
	[[ $arg =~ ^-[^-] ]] && {
		# parse letters into array…
		for i in $(seq 1 ${#arg}); do
			arg[$i]=${arg:$i:1}
		done
		# …and remove original
		unset arg[0]
	}

	# do we have a long option?
	[[ $arg =~ ^-- ]] && {
		# move the option to arg[1] and clean arg[0]
		arg[1]=$arg
		unset arg[0]
	}

	# now we have $arg clean which now contains
	# either a command or command parameter or null
	# $arg[@] needs cleanup to work properly which is
	# done in the loop handling it at last

	# this will parse the bunch-of-options as well
	# as single arguments where the loop is executed
	# only once. 
	# When an option occures demanding a second parameter
	# always $1 is used, shifted and skip_next is increased. 

	# for $arg[@] cleanup
	idx=1

	# only if $arg[0] is unset there are options to handle
	[[ ! ${arg[0]} ]] && {
		for option in "${arg[@]}"; do
				case $option in

					--) echo stop
						stripped=("${stripped[@]}" "$@")
						break 2
						;;

					h|\?|--help) help
						;;

					d|--day) 
						day=$1
						# be grateful with missing leading zero
						[[ ${#day} -eq 1 ]] && day=0$day
						shift
						((skip_next++))
						;;

					m|--month)
						month=$1
						# be grateful with missing leading zero
						[[ ${#month} -eq 1 ]] && month=0$month
						shift
						((skip_next++))
						;;

					y|--year)
						year=$1
						# be grateful with missing leading zero
						[[ ${#year} -eq 1 ]] && year=0$year
						shift
						((skip_next++))
						;;

					D|--date)
						date=$1
						shift
						((skip_next++))
						;;

					Y|--yesterday) 
						date=$(date -d 'yesterday' +%F)
						echo
						;;

					a|--amamedis) echo set amamedis
						amamedis=true
						;;

					"") # ignore empty
						;;

					*) echo unrecognized option: \"-$option\"
						;;

				esac
		# cleanup!
		unset arg[$((idx++))]
		done
	} || {
		# not an option or bunch.
		# store command or command parameter
		stripped=("${stripped[@]}" "$arg")
	}
done

# assemble date
# if date is set, other options -dmy are ignored.
if [[ $date ]]; then
	# sanitize
	date=$(date -d "$date" +%F)
else
	date=$(date -d "${year:-$(date +%y)}${month:-$(date +%m)}${day:-$(date +%d)}" +%F)
fi

[[ $? -ne 0 ]] && {
	echo error setting date
	exit -1
}

echo $date
echo amamedis is ${amamedis:-not set}
echo stripped is ${stripped[@]}
echo stripped length is ${#stripped[@]}

# we are done parsing the options.
# parse command

for command in ${stripped[@]}; do
	echo got $command
	
	case $command in

		*([0-9])) echo dur
			duration=${stripped[0]}
			echo $duration
			unset stripped[0]
			comment=${stripped[@]}
			;;

		*([0-9])-*([0-9])) echo froto
			fromto=${stripped[0]}
			echo $fromto
			unset stripped[0]
			comment=${stripped[@]}
			;;

		parse) echo parse.
			;;

		report) echo report.
			;;
	esac

echo fromto $fromto duration $duration comment $comment
done


# vim: ai sw=4 sts=4 ts=4 noexpandtab
