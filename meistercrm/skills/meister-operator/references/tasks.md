# Tasks

[Skill index](../SKILL.md) · [Approval Gates](approval-gates.md)

Use `list_tasks` by lead or agent. Include `include_resolved: true` to search closed tasks and continue with `next_offset` when returned. Match the task by message, lead and due date, then use `get_task` with its `task_id`. The following CRM controls are available if a tool is missing.

| Action | Steps in MeisterCRM | Check |
| --- | --- | --- |
| Find a task | Open **Tasks** or the lead’s task overview. Identify it by the lead, assigned agent, message and due date. For a completed task, look in the resolved view. | Confirm the correct task when several have a similar message. |
| Create with `create_task` | Choose **Add Task** on the board or the **+** in a lead’s task overview. Check the lead and assigned agent, choose the due date and time, enter the message, and choose a task type if needed. Submit the task. | Find the new task on the correct lead. Verify the owner and due time in the intended time zone. |
| Edit with `update_task` | Open the task card’s **… → Update**, change the intended values and save. The existing task keeps its original lead. | Reopen the task and verify the changed fields. Updates can notify the assigned agent or synchronize a connected calendar. |
| Complete with `resolve_task` or reopen with `reopen_task` | Choose **… → Resolve** on an active task. Use **Active** on a resolved task to reopen it. | Confirm that it appears in the corresponding view. Resolving a task retains its record. |

If the user asks to delete a task, explain that tasks can only be closed by resolving them. Offer **Resolve** and let the user choose. Standalone task deletion is outside scope even with approval. If the lead is known, give the user its [CRM link](leads.md#find-the-right-lead) to reach the task overview.

For a new task, provide the lead ID, `task_msg` and `task_due_date` including the time zone. Select **Tasks → View** to look up a named task type with `list_task_types`. Select **Create** or **Edit** for the intended change. For an edit, send `task_id` and the requested changes. For an uncertain create or update, search the lead’s tasks first and report any ambiguity.

To remove a due date with `update_task`, send `task_id` and `clear_due_date: true`. To remove the task type, send `task_id` and `clear_task_type: true`. Reread the task to verify that the selected field is empty and that the other field still has its prior value if it was omitted.
