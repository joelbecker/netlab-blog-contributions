+++
title = "Data Fusion with recordlinkage: Merging linked dataframes"
description = "The new recordlinkage Data Fusion API merges dataframes and handles data conflicts."
date = 2018-01-02T12:00:00Z
author = "Joel Becker"
+++

<!-- Set up MathJax -->
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>

<script type="text/x-mathjax-config">
  MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
</script>

<!-- Set up html toggle -->

<script>
function toggleShow(id) {
    var x = document.getElementById(id);
    if (x.style.display === 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }
}
</script>

<script>
var hidden = ['df_a', 'df_b', 'data_1', 'data_2', 'data_3', 'data_4']
function onloadHideElems() {
  hidden.forEach(toggleShow)
}
window.onload = onloadHideElems;
</script>

<!-- Post Content -->

Welcome to the fifth installment of NetLab's tutorial series on the [_recordlinkage_](https://github.com/J535D165/recordlinkage) Python package. Each tutorial covers a specific stage of the data integration workflow. The topics and links for each tutorial are included below:

1. [Data Pre-processing](http:/2017/07/05/2017-07-05-preprocessing/)
2. [Indexing](http:/2017/07/18/2017-07-18-indexing/)
3. [Record Comparison](http:/2017/07/18/2017-07-18-comparisons/)
4. Classification (Coming soon...)
5. [Data Fusion](http:/2018/01/02/2018-01-02-data-fusion/)
6. Evaluation (Coming soon...)

# IMPORTANT DISCLAIMER

This is a draft tutorial, which will remain unpublished until in-progress features of the `recordlinkage` package are added into the official distribution of `recordlinkage`. In particular, I'd like to highlight a things:
* The data fusion extension for `recordlinkage` is currently unavilable in the official distribution. Unfortunately, there is not a stable / up-to-date version of these features.
* The follow-up articles discussed in the "preliminaries" section have not yet been written.

# Preliminaries

This tutorial assumes that you have basic knowledge of Python programming, and are acquainted with indexing, comparing, and classifying candidate links with `recordlinkage`. The purpose of this tutorial is to introduce the basic of data fusion to the average `recordlinkage` user. Advanced users may find our follow-up tutorials, [Data Fusion with recordlinkage: Conflict handling for power-users](http:/2018/01/02/2018-01-02-conflict-handling/) and [Data Fusion with recordlinkage: a Developer's Guide](http:/2018/01/02/2018-01-02-fuse-dev/), helpful for getting the most out of these tools.

# What is Data Fusion?

Data integration using `recordlinkage` is all about candidate links — pairs of data frame rows that might refer to the same real world entity. The data indexing stage creates candidate links and excludes obvious non-matches. The data comparison stage compares the candidate links’ features. The classification stage decides whether a candidate link is a true match, or not.

NetLab is pleased to introduce a brand new `recordlinkage` module which implements the final stage of the data integration process: **data fusion**. In the data fusion stage, candidate links are integrated into new data frame rows, creating a new data frame which includes information from both original sources. The new data frame may contain a greater breadth of information than the original data sources, or may incorporate information from both sources using one of several conflict handling strategies.

In this tutorial, we will demonstrate the data fusion process using two data sets. The first is a small subset of the [Global Research Identifier Database (GRID)](grid.ac) database of international research organizations.

[data_1]()

The second is a small dataset scraped from the university reviews website [UniRank](https://www.4icu.org/). The GRID dataset is well-curated and high-quality. The UniRank data may contain scraping errors, and doesn't have a well-defined data schema. These issues will be taken into account when deciding how to manage conflicting data.

[data_2]()

Note: This tutorial only covers how to fuse links from two separate data frame. As of writing, `recordlinkage` does not implement data fusion for deduplicating data frames.

# Handling Conflicting Data

When linking two data frames, a candidate link is pair of data frame rows from different sources which may refer to the same real-world entity. To perform data fusion on a set of candidate links, we need to answer the following question: what process should we use to turn a pair of rows (the candidate link) into a single row?

The easiest way to do this is simply to include all data from both sources.

[data_3]()

However, this isn't a terribly useful data product. We need to account for redundant names, address, and dates which may not be the same. A useful data product would only contain the highest-quality information from the original data sources. To do this, we will need to decide upon **conflict handling strategies** for each redundant data field. A conflict handling strategy is a set of rules for choosing a canonical value from a set of conflicting values. Examples of conflict handling strategies are choosing a random value, choosing a value from a trusted source, or discarding conflicting values.

`recordlinkage` implements a number of popular conflict handling strategies described in the conflict handling literature, plus some highly flexible homebrew strategies:

<table>
<thead>
<tr><th>Strategy                      </th><th>Description                                                                                                                   </th></tr>
</thead>
<tbody>
<tr><td>Trust Your Friends       </td><td>Specify a trusted source, whose values will be prioritized over the less trusted source.                                      </td></tr>
<tr><td>No Gossiping             </td><td>If the values match keep them. If there is a conflict, no value is kept. A very conservative strategy.                        </td></tr>
<tr><td>Roll the Dice            </td><td>Choose a random value.                                                                                                        </td></tr>
<tr><td>Cry With the Wolves      </td><td>Take a vote and use the most common value.                                                                                    </td></tr>
<tr><td>Pass It On               </td><td>Don't handle conflicting values. Instead, pass on all of the options in a collection and handle them later.                   </td></tr>
<tr><td>Meet in the Middle       </td><td>Aggregate conflicting numerical values. For example, take the mean of the observed values.                                    </td></tr>
<tr><td>Keep Up to Date          </td><td>Choose the most recently updated value by comparing timestamps.                                                               </td></tr>
<tr><td>Choose by Scored Value   </td><td>Choose the value that scores the highest (or lowest) on a user-specified scoring function.                                    </td></tr>
<tr><td>Choose by Scored Metadata</td><td>Choose the value with a corresponding metadata value that scores the highest (or lowest) on a user-specified scoring function.</td></tr>
</tbody>
</table>

<!-- Data conflicts paper -->

# The Mechanics of Data Fusion

A given stage of `recordlinkage`'s data integration process has three steps:

1. Initialize an instance of the appropriate `recordlinkage` class.
2. Build up a set of instructions.
3. Specify runtime parameters and execute those instructions.

In practice, this looks like the following:

```python
# Initialize an instance of the appropriate `recordlinkage` class.
fuse = rl.FuseLinks()

# Build up a set of instructions.
fuse.roll_the_dice('grid-name', 'scraped-name')

# Specify runtime parameters and execute those instructions.
fuse.fuse(candidate_links, df_a, df_b, predictions=preds, njobs=8)
```

This may seem backwards to you — why are you passing data inputs at the _end_ of your code? However, building a complete set of instructions independent of your data means that those instructions may be reused on other data with similar schemas, facilitates parallelizing computation, and opens the door for more elegant data integration pipelines.

Even though these inputs appear at the end of this code, they are crucial for understanding how to build up the instructions you write to specify how to handle conflicting data values. Here's what each input means:

* `candidate_links` is a `pandas.MultiIndex` containing the set of candidate links generated in the data indexing stage.
* `df_a`
* `df_b`
* `predictions`
* `njobs`
