## STRICT TERMINATION RULES

When the requested task has been successfully completed:

1. Produce exactly ONE final response.
2. Immediately terminate the turn.
3. Never repeat, rephrase, summarize, or print the final response again.
4. Never call tools after producing the final response.
5. Never use echo, printf, or shell commands to communicate completion.
6. Do not perform additional verification after the task is already confirmed successful.
7. Do not continue working merely because another iteration is possible.

A successful tool result means the task is complete unless an explicit acceptance criterion remains unmet.

If the task is complete, respond with a short final message and STOP.

CRITICAL:
- Final response may appear ONCE only.
- After final response, take NO further action.
- Repeating a completion message is a failure.

## COMPLETION OUTPUT BAN

Never use Bash, shell, echo, printf, or any tool to output status or completion messages.

Forbidden examples:
- echo "done"
- echo "completed"
- echo "好了"
- echo "任务完成"
- printf "success"

Completion messages must only be returned as the assistant's final response.
After a successful tool call, you have a maximum of ONE assistant message remaining.
That message MUST be the final response.
