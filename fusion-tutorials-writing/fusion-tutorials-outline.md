# Data Fusion Tutorials

It's pretty clear that this should be a set of several tutorials. The surface level of `rl.Fuse` is pretty simple to grasp. However, there are a lot of edge cases that should be documented before I'm done with the project.

Developing these tutorials will not be particularly difficult. I know the data fusion API literally inside and out, and it is more tangible than indexing candidate links.

## Data Fusion Tutorial

Basic overview of the data fusion API. How do you initialize a `FuseLinks` object? What are the basics of using the conflict resolution strategies implemented by `recordlinkage`? Tie breaking. How do you run the data fusion process? Logging. Efficiency (`keep_original` vs. others). Multiprocessing and `n_cores`. Output results. (Provide a brief note that it will automatically handle column names.)

## Conflict Resolution Tutorial

An in-depth look at the strategies implemented in the `recordlinkage` API. A look at all of the conflict resolution functions implemented in `recordlinkage.algorithms.conflict_resolution`. Show how to queue a custom conflict resolution job using the generic `resolve` API.

Talk about how to write your own conflict resolution function. What determines the parameter list? How do you choose which parameters to include? Tie breaking.

## Data Fusion Implementation Tutorial

Understanding the nuts and bolts of what's going on under the surface. This is important reading for power users and contributors. Look inside `_make_resolution_series`. Look at the conflict resolution tuple-of-tuples format to understand what you're getting.

Other implementation details? Conflict resolution?
