CC=gcc
PYTHON_VERSION=3.10
PYTHON_INCLUDE=$(python${PYTHON_VERSION}-config --includes)
PYTHON_LIBS=$(python${PYTHON_VERSION}-config --ldflags | sed 's@/usr/lib[^ ]*libdl.a@@g')

HOST_SRC="./tinyriscv/engine/core.c"
HOST_OUT="./tinyriscv/engine/core.so"

spinner(){
  local pid=$1
  local delay=0.1
  local spin='|/-\'
  local i=0

  while kill -0 $pid 2>/dev/null; do
    printf "\rCompiling C source file %s" "${spin:i++%4:1}"
    sleep $delay
  done
}

$CC -Wall -shared -fPIC $HOST_SRC -o $HOST_OUT $PYTHON_INCLUDE $PYTHON_LIBS &

compile_pid=$!
spinner $compile_pid
wait $compile_pid

echo -ne "\r\033[KCompiled Successfully!\n"
