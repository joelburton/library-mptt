Design
======

Our Design: Maintain a Path
---------------------------

This project updates a "path" field on the model so that every object in the tree knows its
URL path.

This makes finding the right object constant time, regardless of tree size, depth, or similarity
of nodes.

This requires modifying the database. It also means that every time a folder is renamed, an
additional write needs to be done to every document/folder below that. For a renaming of a
high-level node in a large tree, this could fire off hundreds or thousands of database writes.

Therefore, this design is best for smaller trees, or where higher level nodes are renamed less
frequently.

TODO: we could do our updating in one SQL, perhaps, by matching that the path starts with the
path of the renamed object. When used with an index that is fast for starts-with, this could
be very speedy.

Alternate Design: Ditch MPTT, use PG's `ltree`
----------------------------------------------

We could keep the same "path" field on the model but store this as a PostgreSQL `ltree` field
(http://www.postgresql.org/docs/9.4/static/ltree.html). We would no longer use `djang-mptt`.

This would keep the fast matching for lookup. It would also keep fast queries for things like
breadcrumbs, finding-descendents, etc (though we'd have to write our own functions for this).

Renaming a high-level node would still mean re-writing everything below it -- but since we're
no longer updating all of the MPTT fields, general adds/edits/deletes would now happen in
constant time.

The main downside here is the creating the drilldown tags and how this would require PostgreSQL.

Alternate Design: Recurse to Object
-----------------------------------

Another design: split the URL path and find the object by searching for each item.

This does not require modifying the database. It does not slow down adding or changing of objects
from vanilla MPTT.

It does make searches fire off a new query for each depth of the tree. For trees deeper than a
few levels, this will make viewing the site inefficient.

Alternative Design: Unique Slugs, Ignore Path
---------------------------------------------

The slugs could be made unique and we could ignore the entire path but the end slug.

So::

  /js/angular/routing/routing-ex

could would work by just looking for `routing-ex`.

This does mean that::

  /js/ng/routes/routing-ex

Would find the same object, of course.

This does not slow down adding/editing the tree and does make for lookups as fast as ours.

It would make it a pain as we want to use folders/documents with similar names, like
"examples" or "overview". These would need unique slugs.

Alternative Design: Find By Slug, Confirm Path
----------------------------------------------

A similar idea would be to search for all objects matching the final slug, then hand-check
that candidate list for which one had the matching path.

For example, given::

  /js/overview
  /js/other/
  /python/overview
  /python/library

A URL of `/js/overview` would find both `overview` objects. We could then calculate the path
of each, find the matching path, and use that object.

This does not slow down adding/editing the tree. It does add a query for non-correct-candidate.

If names are widely reused, this would slow down search (potentially quite a bit: if every
folder had a document called 'overview' in it, we'd fire off one query for every folder
in the entire tree, regardless of tree-height/our depth)

