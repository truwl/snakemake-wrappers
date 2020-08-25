"""Snakemake wrapper for Varscan2 mpileup2indel"""

__author__ = "Thibault Dayris"
__copyright__ = "Copyright 2019, Dayris Thibault"
__email__ = "thibault.dayris@gustaveroussy.fr"
__license__ = "MIT"

import os
import os.path as op

# Gathering extra parameters and logging behaviour
log = snakemake.log_fmt_shell(stdout=False, stderr=True)
extra = snakemake.params.get("extra", "")

# In case input files are gzipped mpileup files,
# they are being unzipped and piped
# In that case, it is recommended to use at least 2 threads:
# - One for unzipping with zcat
# - One for running varscan
pileup = (
    " cat {} ".format(snakemake.input[0])
    if not snakemake.input[0].endswith("gz")
    else " zcat {} ".format(snakemake.input[0])
)

# Building output directories
output_dir = op.dirname(snakemake.output[0])
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

os.system(
    f'/bin/bash -c "varscan mpileup2indel '  # Tool and its subprocess
    f"{extra} "  # Extra parameters
    f"<( {pileup} ) "
    f"> {snakemake.output[0]} "  # Path to vcf file
    f'{log}"'  # Logging behaviour
)
