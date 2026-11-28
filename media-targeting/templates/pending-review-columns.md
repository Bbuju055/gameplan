# Pending-review file — fixed column layout

Where approved new names and suggested corrections wait for the log owner, written only through
the reporter-list skill. Where it lives depends on `media_log.source`:

- **m365** and **file**: a separate CSV file (`pending_review.file_name`, default
  "Media Log - Pending Review.csv") in the same folder as the media log; Excel opens it.
  reporter-list creates it, with exactly the header row below, the first time it has a row to
  write, then appends by whole-file replace (read the file, add rows, write it back).
- **google**: a new Sheet per run, named "<file_name without extension> <YYYY-MM-DD>", created
  with this header row, because the Drive connector cannot append rows to an existing Sheet.
- **suite**: none. Approved names go straight into the suite's own list.

The log owner promotes rows into the main log on their own schedule and deletes them from here.

| Column | Content |
|---|---|
| Date added | the day the operator approved the row |
| Reporter | name |
| Outlet | verified from bylines; for a health-check row, the outlet the latest byline shows |
| Beat | as evidenced by the cited articles; for a health-check row, the beat the latest bylines show |
| Email | how to reach them, publicly sourced only and labelled: a published email, the outlet's tips or desk address, a contact form, or a public handle; "not found: verify manually" only when no way to reach them of any kind was found, never beside one that was |
| Geography | where the outlet publishes from or the reporter is based, as the outlet or the article shows it; never assumed from the language it is written in; empty when nothing shows it |
| Source | "Discovery", "Source request", "Media list" ("Media list: one article" for a name added on one article, "Media list: wrote about the client" for one added because they wrote about the client), or a health-check finding: "Health check: moved", "Health check: left beat", "Health check: left journalism" |
| Evidence | the citation links (the receipts that justified the row) |
| Campaign | client - release title; for a media list, client or topic - "media list" |
| Status | left blank for the log owner ("added" / "rejected" / notes) |

A health-check row is a suggested correction to a name already in the log: it never changes the
log itself. The plugin never edits the Status column and never removes rows — append only.
