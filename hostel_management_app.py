import streamlit as st
import pandas as pd
import qrcode
from PIL import Image


# Load CSV data (assuming CSV file is in the same directory as the app)
def load_student_data():
    # Load student data from CSV
    df = pd.read_csv("students.csv")
    return df


# Function to get student details by name
def get_student_details(name, df):
    student = df[df['student_name'].str.lower() == name.lower()]
    # print(student)
    if not student.empty:
        return student.iloc[0]  # Return the first match (assuming names are unique)
    else:
        return None


def get_qr_code(student_id):
    if student_id < 26:
        return "sbi.jpg"
    elif 26 <= student_id < 52:
        return "jsbs.jpg"
    else:
        return "jsb.jpg"

# Function to handle rent based on single parent status
def calculate_rent(room_number, is_single_parent):
    # Parking rooms (1, 2, 3) have a rent 100 INR less

    if room_number in [1, 2, 3]:
        if is_single_parent=='yes':
            rent = 1500
            return rent
        else:
            rent = 1600
            return rent
        # rent = 1500 if is_single_parent else 1600  # Rent for parking rooms with a single parent
    else:
        # rent = 1600 if is_single_parent else 1700  # Rent for other rooms
        if is_single_parent=='yes':
            rent = 1600
            return rent
        else:
            rent = 1700
            return rent
    # return rent


# Streamlit App
def hostel_management_app():
    st.title("Shelke Niwas")

    st.sidebar.header("Student Information")

    # Load student data from CSV
    df = load_student_data()

    # Student Name input
    student_name = st.text_input("Enter your Name")

    if student_name:
        # Fetch student details from the CSV
        student_details = get_student_details(student_name, df)


        if student_details is not None:
            room_number = student_details['room_no']
            student_id = student_details['student_id']

            is_single_parent = student_details['isSingleParent']

            # Calculate the rent based on single parent status
            rent_due = calculate_rent(room_number,is_single_parent)
            qr_code_file = get_qr_code(student_id)

            st.sidebar.subheader("Student Details")
            st.sidebar.write(f"Name: {student_name}")
            st.sidebar.write(f"Id: {student_id}")
            st.sidebar.write(f"Room Number: {room_number}")
            st.sidebar.write(f"Rent Due: {rent_due} INR")

            st.subheader("Payment QR Code")
            qr_code_img = Image.open(qr_code_file)
            st.image(qr_code_img, caption="Scan this QR code to pay")
        else:
            st.write("Student not found. Please select your details from the dropdown menus.")

            # Dropdown to select room number
            room_numbers = df['room_no'].unique()
            selected_room = st.selectbox("Select your Room Number", options=room_numbers)

            if selected_room:
                # Dropdown to select student name based on selected room number
                students_in_room = df[df['room_no'] == selected_room]['student_name']
                selected_student = st.selectbox("Select your Name", options=students_in_room)

                if selected_student:
                    # Fetch student details again based on selected name
                    student_details = get_student_details(selected_student, df)

                    if student_details is not None:
                        room_number = student_details['room_no']
                        student_id = int(student_details['student_id'])  # Ensure student_id is an integer
                        is_single_parent = student_details['isSingleParent']

                        # Calculate the rent based on single parent status
                        rent_due = calculate_rent(room_number, is_single_parent)

                        # Get the appropriate QR code based on student_id
                        qr_code_file = get_qr_code(student_id)

                        st.subheader("Student Details")
                        st.write(f"**Name**: {selected_student}")
                        st.write(f"**ID**: {student_id}")
                        st.write(f"**Room Number**: {room_number}")
                        st.write(f"**Rent Due**: {rent_due} INR")

                        # Display the appropriate QR code for payment on the main screen
                        st.subheader("Payment QR Code")
                        qr_code_img = Image.open(qr_code_file)
                        st.image(qr_code_img, caption="Scan this QR code to pay", use_column_width=True)


# Run the Streamlit app
if __name__ == "__main__":
    hostel_management_app()
    # df = load_student_data()
    # print(df.columns)
