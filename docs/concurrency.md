<h1>Concurrency Cases</h1>

<h2>Case 1</h2>

In this case there is a read skew phenomenon, as transaction 1 first reads the battle, only for transaction 2 to determine and update the battle, reading that character ID 2 has won, where transaction 1 reads None. In our code we fixed it by locking the row before updating to ensure no two transactions can collide at once. Down below is the concurrency issue before updating the code.

<img width="561" alt="Screenshot 2025-05-28 001358" src="https://github.com/user-attachments/assets/7f435f9b-4c27-45e0-a621-b67ba0c2f633" />

<h2>Case 2</h2>

There is a write skew phenomenon as transaction 1 attempts to insert the same character by the same user. This issue is resolved by putting unique constraints on the user id and name composite key to ensure users don't have this concurrency issue of trying to update the same character. The code will implement some lock or update to ensure this phenomenon doesn't occur.

<img width="800" alt="Screenshot 2025-05-28 004818" src="https://github.com/user-attachments/assets/8f53240a-a16d-4ebb-9ace-2e8b94e96307" />

<h2>Case 3</h2>

In this case there is a lost update phenomenon, as transaction 1 and transaction 2 both vote for the same battle at the same time for User ID 1. The problem is that when Transaction 1 votes first for character ID 1, followed in succession by Transaction 2 for character ID 2. It will lose the first transaction and keep the vote for character ID 2. THis is fixed by using a FOR UPDATE again, which would prevent two transaction from happening at the same time by locking the updated row.

<img width="448" alt="Screenshot 2025-05-28 004651" src="https://github.com/user-attachments/assets/5cc609fc-453a-4741-b04e-560d65c0c8a2" />
