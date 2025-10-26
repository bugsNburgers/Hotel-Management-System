Of course\! Here is the formatted version for your README file.

-----

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

  * **MySQL**: Make sure you have MySQL installed and the server is running.
  * **Python 3**: Ensure Python 3 is installed on your system.

-----

### 📦 Installation & Setup

#### 1\. Database Setup

First, create the database schema and populate it with initial data.

1.  **Create the schema**: Open your terminal and run the following command. You will be prompted for your MySQL root password.

    ```bash
    mysql -u root -p < schema.sql
    ```

2.  **Seed the database**: Run the seed script to add initial data.

    ```bash
    mysql -u root -p < seed.sql
    ```

    > **Note**: The application uses the `root` user by default. You can create a different user and update the configuration if you prefer.

#### 2\. Python Environment

Set up a virtual environment and install the required Python packages.

1.  **Create and activate the virtual environment**:

      * **On Windows**:
        ```cmd
        python -m venv venv
        venv\Scripts\activate
        ```
      * **On Linux/macOS**:
        ```bash
        python -m venv venv
        source venv/bin/activate
        ```

2.  **Install dependencies**:

    ```bash
    pip install mysql-connector-python ttkbootstrap
    ```

#### 3\. Environment Variables (Optional)

You can either set environment variables or edit the default database connection values directly in `main_full.py`.

  * **On Linux/macOS**:

    ```bash
    export DB_HOST=localhost
    export DB_USER=root
    export DB_PASS=yourpassword
    export DB_NAME=hms
    ```

  * **On Windows (cmd)**:

    ```cmd
    set DB_HOST=localhost
    set DB_USER=root
    set DB_PASS=yourpassword
    set DB_NAME=hms
    ```

-----

### ▶️ Running the Application

With the environment set up, you can now run the GUI.

```bash
python main_full.py
```

#### Login Credentials

Use the seeded account to log in:

  * **Username**: `admin`
  * **Password**: `admin123`

-----

### ✅ What to Test

Here are a few scenarios to test the application's core functionality.

#### Manage Rooms

1.  Go to **Manage Rooms**.
2.  Add a new room (e.g., room `301`).
3.  Delete an existing room.
4.  Verify that an audit log with the event `ROOM_DELETE` was created in the **Audit Logs** section.

#### Manage Customers (Check-In / Check-Out)

1.  Go to **Manage Customers**.
2.  Fill in the customer details (**Name**, **Proof**, **Checkin**, **Checkout**, and select a **Vacant** room).
3.  Click **Check In**. This executes a stored procedure that:
      * Checks room vacancy.
      * Locks the row.
      * Inserts the new customer.
      * Sets the room status to `Occupied`.
      * Creates an audit log.
      * A success message with the new Customer ID (`CID`) will be displayed.
4.  Select the same customer from the list and click **Check Out**. This triggers an `UPDATE` operation, and the `tr_customer_status_after_update` trigger will:
      * Set the room's `vacancy` status back to `Vacant`.
      * Insert a new audit log for the checkout event.

#### Booking & Payment

1.  Navigate to the **Booking & Payment** section.
2.  Create a new booking and payment. This calls a procedure that atomically inserts both records and returns a booking ID.

#### Reports & Logs

  * **Reports**: Check the occupancy and revenue reports to see aggregated data.
  * **Audit Logs**: View the logs to see a history of events automatically recorded by triggers and procedures.