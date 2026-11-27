# Catalog import and export

Read [Approval Gates](../approval-gates.md) at the start of every run. Use the **Catalog** import and export controls in MeisterCRM for spreadsheets. The connector’s individual item and rate tools operate on identified records. Keep file validation, attachment and bulk import in the CRM. Ask whether the user wants to attach a rate sheet under **Documents**, import its structured rows into the catalog, or download existing catalog data.

## Choose the target

| Import type | For an existing item, select | Verify in the file |
| --- | --- | --- |
| Hotel | The property, including its rooms | Hotel and location, room names and capacity, seasons and supplements |
| Activity | The activity | Name, location, duration, currency and price bands |
| Transfer | The transfer | Service, capacity, daily or taxi, route and cost |
| Flight | The airline | Route direction, times, operating frequency and fare |
| Add-on | The add-on | Name, subtype, features, placement, pricing basis and rate |
| Location | The location | Fee name, per-person or group basis, currency, dates and applicable overnight or camping cost |

**One existing item.** Open the saved item's drawer and choose **Import** on its master tab when available. For hotel rates, use **Hotel** in the room/hotel drawer. This adds rates to the property's existing rooms. Check the hotel, location, room names and any overlap with current rates before committing. To change the price of an existing rate, use its [contract row](contracts.md). If the file names a room the hotel does not yet have, resolve the discrepancy first.

**Multiple or new items.** Use the Catalog tab's actions menu and choose **Import**, then select the type and language. This broader operation can create masters and children. Keep a request for a single saved item on that item's drawer.

## Validate and import

1. Download the current template for the selected type or start from a compatible export. Keep its headers. Use CSV or XLSX. For XLSX, put the data on the first worksheet. If validation reports a file-size, row or column limit, adjust the file to the reported limit. Keep dependent records together when splitting a file and validate each part before importing.
2. Select the language, type, file and target, then upload for validation. Review the results. When an error is reported, identify the row, field and reason, download the error report if useful, correct the file and validate again. Changing the target, language or file requires another validation.
3. After validation, explain which records the import will affect, the target workspace and item, and any warnings. Obtain explicit approval for that exact file and target before **Continue to Import**. Selecting or validating the file alone authorizes no import.
4. Read the result, reload the affected items, and compare names, parent items, dates, rate counts and currencies with the submitted file. If the import is interrupted or partly succeeds, inspect the saved rows before considering a retry.

If the committed import created catalog items, finish the [description and picture checks](master-records.md#descriptions-and-pictures-for-new-items) on those saved records, including newly created rooms.

## Export

- **One item.** Open its saved drawer and choose Export and the offered format. For all rooms/rates of one property, export the **hotel**.
- **A filtered catalog view.** Select the type and filters, check the matching items, then open the tab's actions menu and choose the CSV or XLSX **Export All** option. The action uses the current tab and its filtered results. Bulk-delete checkboxes do not define this export. For a specific subset, use a filter that yields exactly the requested items, individual drawer exports, or a tool that explicitly accepts a selection. If the filter matches nothing, report that result.
- **The full catalog for one type.** Clear unintended filters and verify the intended ownership and record scope before exporting. The Countries tab offers no catalog file action. Check the downloaded format, language and item coverage. Returning the file to the requester and sending it elsewhere are separate actions.

[Back to the skill index](../../SKILL.md)
