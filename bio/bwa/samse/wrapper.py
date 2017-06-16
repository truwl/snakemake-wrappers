"""Snakemake wrapper for bwa sampe."""

__author__ = "Julian de Ruiter"
__copyright__ = "Copyright 2017, Julian de Ruiter"
__email__ = "julianderuiter@gmail.com"
__license__ = "MIT"


from snakemake.shell import shell


# Extract arguments.
extra = snakemake.params.get("extra", "")

sort = snakemake.params.get("sort", "none")
sort_order = snakemake.params.get("sort_order", "coordinate")
sort_extra = snakemake.params.get("sort_extra", "")

log = snakemake.log_fmt_shell(stdout=False, stderr=True)

# Determine which pipe command to use for converting to bam or sorting.
if sort == "none":

    # Simply convert to bam using samtools view.
    pipe_cmd = "samtools view -Sbh -o {snakemake.output[0]} -"

elif sort == "samtools":

    # Sort alignments using samtools sort.
    pipe_cmd = "samtools sort {sort_extra} -o {snakemake.output[0]} -"

    # Add name flag if needed.
    if sort_order == "queryname":
        sort_extra += " -n"

elif sort == "picard":

    # Sort alignments using picard SortSam.
    pipe_cmd = ("picard SortSam {sort_extra} INPUT=/dev/stdin"
                " OUTPUT={snakemake.output[0]} SORT_ORDER={sort_order}")

else:
    raise ValueError("Unexpected value for params.sort ({})".format(sort))

# Run command.
shell(
    "(bwa samse"
    " {extra}"
    " {snakemake.params.index}"
    " {snakemake.input.sai}"
    " {snakemake.input.fastq}"
    " | " + pipe_cmd + ") {log}")
