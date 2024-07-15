#!/usr/bin/env bash

#
# DISPATCHER
#
# This is a wrapper that executes python scripts with the appropriate python
# build.  
#
# Useful debugging args:
# 
#   --DISPATCH-DEBUG to see what exactly it's doing.
#   --DISPATCH-FIND  to see what target python script is getting invoked
# 

NAME=$(basename $0)
DISPATCH_DIR=$(dirname $(readlink -f $0))

PYTHON3="${DISPATCH_DIR}/venv/bin/python3"
TARGET_PY="${DISPATCH_DIR}/${NAME}.py"
DRY_RUN=0
FIND_ONLY=0

PASS_THROUGH_ARGS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        --DISPATCH-DEBUG)
            DRY_RUN=1
            ;;
        --DISPATCH-FIND)
            DRY_RUN=1
            FIND_ONLY=1
            ;;
        *)
            PASS_THROUGH_ARGS+=("$1")
            ;;
    esac
    shift
done

if [[ -e "${TARGET_PY}" ]]; then
    COMMAND="${PYTHON3} ${TARGET_PY} ${PASS_THROUGH_ARGS[@]}"
    if [[ "$DRY_RUN" -eq 0 ]]; then
        COMMAND="${PYTHON3} ${TARGET_PY} ${PASS_THROUGH_ARGS[@]}"
        exec ${COMMAND}
    elif [[ "$FIND_ONLY" -eq 0 ]]; then
        ME=$(readlink -f $0)
        echo "Hello from dispatch!"
        echo
        echo "Dispatcher:    ${ME}"
        echo "Invoker:       $0"
        echo "Python:        $PYTHON3"
        echo "Target script: $TARGET_PY"
        echo
        echo "Without --DISPATCH-DEBUG, I would have exec'd:"
        echo
        echo "   $ ${COMMAND}"
    else
        echo "${TARGET_PY}"
    fi
fi
