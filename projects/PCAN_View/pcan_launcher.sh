#!/usr/bin/env bash
# PCAN-View style launcher and setup helper
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UI_PY="$ROOT_DIR/ui/pcan_view.py"

CSI_RESET="\e[0m"
CSI_BOLD="\e[1m"
CSI_RED="\e[31m"
CSI_GREEN="\e[32m"
CSI_YELLOW="\e[33m"

die(){ echo -e "${CSI_RED}Error:${CSI_RESET} $*"; exit 1; }

check_cmd(){ command -v "$1" >/dev/null 2>&1 || die "$1 is required but not installed."; }

list_can_ifaces(){
  ip -o link show | awk -F': ' '{print $2}' | grep -E '^can|^vcan' || true
}

show_status(){
  echo -e "${CSI_BOLD}Detected CAN interfaces:${CSI_RESET}"
  list_can_ifaces | while read -r ifc; do
    if [ -z "$ifc" ]; then continue; fi
    state=$(ip -details link show "$ifc" 2>/dev/null | awk '/state/ {print $0; exit}')
    echo -e "  - ${CSI_YELLOW}$ifc${CSI_RESET} : ${state:-unknown}"
  done
}

bring_up(){
  local ifc=$1; local bitrate=$2
  sudo ip link set "$ifc" type can bitrate "$bitrate" || return 1
  sudo ip link set "$ifc" up || return 1
  echo "Interface $ifc up at $bitrate bps"
}

bring_down(){
  local ifc=$1
  sudo ip link set "$ifc" down
  echo "Interface $ifc down"
}

launch_ui(){
  if [ ! -f "$UI_PY" ]; then
    die "UI not found at $UI_PY"
  fi
  python3 "$UI_PY"
}

send_test_frame(){
  check_cmd cansend
  read -rp "Interface (e.g. can0): " ifc
  read -rp "Frame (e.g. 580#1122334455667788): " frame
  cansend "$ifc" "$frame"
}

print_menu(){
  clear
  echo -e "${CSI_BOLD}PCAN-View Launcher${CSI_RESET}"
  echo
  show_status
  echo
  echo "1) List interfaces"
  echo "2) Bring interface up"
  echo "3) Bring interface down"
  echo "4) Launch GUI (Python)"
  echo "5) Start candump (live dump)"
  echo "6) Send test frame (cansend)"
  echo "7) Reset interface (down/up)"
  echo "8) Exit"
  echo
}

while true; do
  print_menu
  read -rp $'Choose an option: ' opt
  case "$opt" in
    1)
      echo
      list_can_ifaces || echo "(none)"
      read -rp $'Press Enter to continue'
      ;;
    2)
      read -rp "Interface: " ifc
      read -rp "Bitrate (e.g. 500000): " br
      if [ -z "$ifc" ] || [ -z "$br" ]; then echo "Cancelled"; else bring_up "$ifc" "$br"; fi
      read -rp $'Press Enter to continue'
      ;;
    3)
      read -rp "Interface: " ifc
      [ -z "$ifc" ] && echo "Cancelled" || bring_down "$ifc"
      read -rp $'Press Enter to continue'
      ;;
    4)
      echo "Launching GUI..."
      launch_ui
      ;;
    5)
      check_cmd candump
      read -rp "Interface (can0): " ifc
      if [ -z "$ifc" ]; then ifc=can0; fi
      echo "Starting candump on $ifc (ctrl-c to stop)"
      candump -td -H -x -c "$ifc"
      ;;
    6)
      send_test_frame
      read -rp $'Press Enter to continue'
      ;;
    7)
      read -rp "Interface: " ifc
      read -rp "Bitrate: " br
      [ -z "$ifc" ] && echo "Cancelled" || { bring_down "$ifc"; sleep 1; bring_up "$ifc" "${br:-500000}"; }
      read -rp $'Press Enter to continue'
      ;;
    8)
      echo "Bye"; exit 0 ;;
    *) echo "Invalid option"; sleep 1 ;;
  esac
done
