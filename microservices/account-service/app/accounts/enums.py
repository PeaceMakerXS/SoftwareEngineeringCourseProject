from enum import StrEnum


class TransactionStatus(StrEnum):
	CANCELLED = 'Cancelled'
	PENDING = 'Pending'
	SUCCESSFUL = 'Successful'


class OperationType(StrEnum):
	TRANSFER = 'Transfer'
	PAYMENT = 'Payment'
	WITHDRAWAL = 'Withdrawal'
	DEPOSIT = 'Deposit'
