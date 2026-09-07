#!/usr/bin/env bash
# Make sure the PostgreSQL build prerequisites exist on this machine.
#
# Since PostgreSQL 17 the release tarballs no longer carry pre-generated
# parser/scanner sources, so Bison (>= 2.3) and Flex are required on every
# platform, next to Perl and a C compiler.
#
#   Linux   — runs inside cibuildwheel's manylinux container (AlmaLinux 8 based
#             for manylinux_2_28); bison/flex are not preinstalled there.
#   macOS   — Xcode command line tools ship bison 2.3 and flex 2.6.
#   Windows — handled in the workflow: winflexbison3 via Chocolatey, exported
#             to configure as BISON=win_bison FLEX=win_flex.
set -euo pipefail

need=()
for tool in "${BISON:-bison}" "${FLEX:-flex}" perl; do
    command -v "$tool" >/dev/null 2>&1 || need+=("$tool")
done

if [ ${#need[@]} -eq 0 ]; then
    echo "prepare: bison, flex and perl present"
    exit 0
fi

echo "prepare: missing ${need[*]}"
case "$(uname -s)" in
    Linux)
        if command -v dnf >/dev/null 2>&1; then
            dnf install -y bison flex perl
        elif command -v yum >/dev/null 2>&1; then
            yum install -y bison flex perl
        elif command -v apt-get >/dev/null 2>&1; then
            apt-get update && apt-get install -y bison flex perl
        elif command -v apk >/dev/null 2>&1; then
            apk add --no-cache bison flex perl
        else
            echo "prepare: no known package manager" >&2
            exit 1
        fi
        ;;
    Darwin)
        echo "prepare: expected bison/flex/perl from the Xcode command line tools" >&2
        exit 1
        ;;
    *)
        echo "prepare: install winflexbison and set BISON/FLEX (see the workflow)" >&2
        exit 1
        ;;
esac

bison --version | head -1
flex --version | head -1
