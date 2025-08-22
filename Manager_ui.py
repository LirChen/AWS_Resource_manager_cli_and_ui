import customtkinter as ctk
from botocore.exceptions import ClientError
import os
from Manager import OWNER, create_ec2, connect, manage_ec2, instance_list_ec2, create_s3, create_route53, manage_route53, delete_route53,upload_file_s3, list_s3, delete_s3, list_route53
from click.testing import CliRunner

COLORS = {
    'primary': "#1a1a2e",
    'secondary': "#16213e",
    'accent': "#0f3460",
    'gradient_start': "#667eea",
    'gradient_end': "#764ba2",
    'success': "#00d2ff",
    'warning': "#ff6b35",
    'error': "#ff5e5b",
    'text_primary': "#ffffff",
    'text_secondary': "#b0b3b8",
    'glass': "rgba(255, 255, 255, 0.1)",
    'purple_glow': "#8b5cf6",
    'blue_glow': "#3b82f6"
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            fg_color=COLORS['secondary'],
            border_color=COLORS['accent'],
            border_width=1,
            corner_radius=20
        )

class Button(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            corner_radius=15,
            border_width=1,
            border_color=COLORS['purple_glow'],
            font=("Inter", 14, "bold"),
            height=50,
            hover_color=COLORS['blue_glow'],
            fg_color=COLORS['accent'],
            text_color=COLORS['text_primary']
        )


class ComboBox(ctk.CTkComboBox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            corner_radius=10,
            border_width=2,
            border_color=COLORS['accent'],
            button_color=COLORS['purple_glow'],
            button_hover_color=COLORS['blue_glow'],
            dropdown_hover_color=COLORS['accent'],
            font=("Inter", 12),
            height=40
        )

class Entry(ctk.CTkEntry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            corner_radius=10,
            border_width=2,
            border_color=COLORS['accent'],
            font=("Inter", 12),
            height=40
        )

class Label(ctk.CTkLabel):
    def __init__(self, master, text, size=14, weight="normal", **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            text=text,
            font=("Inter", size, weight),
            text_color=COLORS['text_primary']
        )

class GlowEffect(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            fg_color="transparent",
            border_color=COLORS['purple_glow'],
            border_width=2,
            corner_radius=20
        )

root = ctk.CTk()
root.title("AWS Resource Manager")
root.geometry("1200x900")
root.configure(fg_color=COLORS['primary'])

main_container = Frame(root)
main_container.pack(fill="both", expand=True, padx=30, pady=30)

header_frame = Frame(main_container)
header_frame.pack(fill="x", padx=20, pady=(20, 30))

title_label = Label(header_frame, "AWS Resource Manager", 28, "bold")
title_label.pack(pady=20)

subtitle_label = Label(header_frame, "Manage your AWS resources with style", 14, "normal")
subtitle_label.configure(text_color=COLORS['text_secondary'])
subtitle_label.pack(pady=(0, 10))

tabview = ctk.CTkTabview(main_container)
tabview.pack(fill="both", expand=True, padx=20, pady=20)

ec2_tab = tabview.add("💻 EC2")
s3_tab = tabview.add("🗄️ S3")
route53_tab = tabview.add("🌐 Route53")

tabview.configure(
    corner_radius=20,
    border_width=2,
    border_color=COLORS['purple_glow'],
    segmented_button_fg_color=COLORS['primary'],
    segmented_button_selected_color=COLORS['purple_glow'],
    segmented_button_selected_hover_color=COLORS['blue_glow'],
    segmented_button_unselected_color=COLORS['secondary'],
    segmented_button_unselected_hover_color=COLORS['accent']
)

#ec2
def setup_ec2_tab():
    ec2_header = ctk.CTkFrame(ec2_tab)
    ec2_header.configure(
        fg_color=COLORS['accent'],
        corner_radius=15,
        border_width=1,
        border_color=COLORS['purple_glow']
    )
    ec2_header.pack(fill="x", padx=20, pady=20)

    ec2_title = Label(ec2_header, "💻 EC2 Management", 24, "bold")
    ec2_title.pack(pady=20)

    ec2_subtitle = Label(ec2_header, "Create, manage, and monitor your EC2 instances", 12)
    ec2_subtitle.configure(text_color=COLORS['text_secondary'])
    ec2_subtitle.pack(pady=(0, 20))

    button_container = Frame(ec2_tab)
    button_container.pack(fill="x", padx=20, pady=20)

    ec2_create_btn = Button(
        button_container,
        text="🚀 Create Instance",
        width=300,
        command=open_create_ec2_window
    )
    ec2_create_btn.pack(pady=15)

    ec2_manage_btn = Button(
        button_container,
        text="⚙️ Manage Instance",
        width=300,
        command=open_manage_ec2_window
    )
    ec2_manage_btn.pack(pady=15)

    ec2_list_btn = Button(
        button_container,
        text="📊 List Instances",
        width=300,
        command=open_list_ec2_window
    )
    ec2_list_btn.pack(pady=15)

# s3
def setup_s3_tab():
    s3_header = ctk.CTkFrame(s3_tab)
    s3_header.configure(
        fg_color=COLORS['accent'],
        corner_radius=15,
        border_width=1,
        border_color=COLORS['purple_glow']
    )
    s3_header.pack(fill="x", padx=20, pady=20)

    s3_title = Label(s3_header, "🗄️ S3 Storage", 24, "bold")
    s3_title.pack(pady=20)

    s3_subtitle = Label(s3_header, "Manage your S3 buckets and files with ease", 12)
    s3_subtitle.configure(text_color=COLORS['text_secondary'])
    s3_subtitle.pack(pady=(0, 20))

    button_container = Frame(s3_tab)
    button_container.pack(fill="x", padx=20, pady=20)

    s3_create_btn = Button(
        button_container,
        text="🎯 Create Bucket",
        width=300,
        command=open_create_s3_window
    )
    s3_create_btn.pack(pady=12)

    s3_upload_btn = Button(
        button_container,
        text="⬆️ Upload File",
        width=300,
        command=open_upload_s3_window
    )
    s3_upload_btn.pack(pady=12)

    s3_delete_btn = Button(
        button_container,
        text="🗑️ Delete Bucket",
        width=300,
        command=open_delete_s3_window
    )
    s3_delete_btn.configure(
        fg_color=COLORS['error'],
        hover_color="#ff3838"
    )
    s3_delete_btn.pack(pady=12)

    s3_list_btn = Button(
        button_container,
        text="📋 List Buckets",
        width=300,
        command=open_list_s3_window
    )
    s3_list_btn.pack(pady=12)

# route53
def setup_route53_tab():
    route53_header = ctk.CTkFrame(route53_tab)
    route53_header.configure(
        fg_color=COLORS['accent'],
        corner_radius=15,
        border_width=1,
        border_color=COLORS['purple_glow']
    )
    route53_header.pack(fill="x", padx=20, pady=20)

    route53_title = Label(route53_header, "🌐 Route53 DNS", 24, "bold")
    route53_title.pack(pady=20)

    route53_subtitle = Label(route53_header, "Configure DNS and hosted zones", 12)
    route53_subtitle.configure(text_color=COLORS['text_secondary'])
    route53_subtitle.pack(pady=(0, 20))

    button_container = Frame(route53_tab)
    button_container.pack(fill="x", padx=20, pady=20)

    route53_create_btn = Button(
        button_container,
        text="🎯 Create Hosted Zone",
        width=300,
        command=open_create_route53_window
    )
    route53_create_btn.pack(pady=15)

    route53_manage_btn = Button(
        button_container,
        text="⚙️ Manage Zone",
        width=300,
        command=open_manage_route53_window
    )
    route53_manage_btn.pack(pady=15)

    route53_list_btn = Button(
        button_container,
        text="📊 List Zones",
        width=300,
        command=open_list_route53_window
    )
    route53_list_btn.pack(pady=15)


def create_window(title, size="800x600"):
    window = ctk.CTkToplevel(root)
    window.title(title)
    window.geometry(size)
    window.configure(fg_color=COLORS['primary'])

    window.transient(root)
    window.grab_set()
    window.lift()
    window.focus()

    main_frame = Frame(window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    return window, main_frame

# ec2 functions
def open_create_ec2_window():
    create_ec2_window, main_frame = create_window("🚀 Create EC2 Instance")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "🚀 Create EC2 Instance", 20, "bold")
    title.pack(pady=20)

    form_frame = Frame(main_frame)
    form_frame.pack(fill="x", padx=20, pady=20)

    ami_label = Label(form_frame, "🖥️ Choose AMI:", 14, "bold")
    ami_label.pack(pady=(20, 5))

    ami_dropdown = ComboBox(
        form_frame,
        values=["ubuntu", "amazon-linux"],
        width=300
    )
    ami_dropdown.pack(pady=(0, 20))
    ami_dropdown.set("ubuntu")

    instance_type_label = Label(form_frame, "⚡ Instance Type:", 14, "bold")
    instance_type_label.pack(pady=(20, 5))

    instance_type_dropdown = ComboBox(
        form_frame,
        values=["t3.micro", "t2.small"],
        width=300
    )
    instance_type_dropdown.pack(pady=(0, 20))
    instance_type_dropdown.set("t3.micro")

    submit_button = Button(
        form_frame,
        text="✨ Create Instance",
        width=250,
        command=lambda: create_instance_clicked(ami_dropdown, instance_type_label, instance_type_dropdown,
                                                create_ec2_window)
    )
    submit_button.configure(
        fg_color=COLORS['success'],
        hover_color="#00b8e6"
    )
    submit_button.pack(pady=30)

def create_instance_clicked(ami_dropdown, instance_type_label, instance_type_dropdown, window):
    ami_value = ami_dropdown.get()
    instance_type_value = instance_type_dropdown.get()

    try:
        runner = CliRunner()
        res = runner.invoke(create_ec2, [ami_value, instance_type_value])
        output = res.output.strip()

        if "Instance created:" in output:
            print("Instance created successfully!")
            print(output)
        elif "You can't have more than 2 running instances" in output:
            print("Maximum 2 running instances limit reached")
        elif "No instances created" in output:
            print("No instances created by CLI found")
        else:
            print(f"Result: {output}")

    except Exception as e:
        print(f"Error: {e}")

    window.destroy()

def open_manage_ec2_window():
    manage_window, main_frame = create_window("⚙️ Manage EC2 Instance")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "⚙️ Manage EC2 Instance", 20, "bold")
    title.pack(pady=20)

    form_frame = Frame(main_frame)
    form_frame.pack(fill="x", padx=20, pady=20)

    action_label = Label(form_frame, "🎯 Choose Action:", 14, "bold")
    action_label.pack(pady=(20, 5))

    action_dropdown = ComboBox(
        form_frame,
        values=["start", "stop", "terminate"],
        width=300
    )
    action_dropdown.pack(pady=(0, 20))
    action_dropdown.set("start")

    instances = get_instances_for_combobox()

    instance_label = Label(form_frame, "💻 Choose Instance:", 14, "bold")
    instance_label.pack(pady=(20, 5))

    instance_dropdown = ComboBox(
        form_frame,
        values=instances,
        width=350
    )
    instance_dropdown.pack(pady=(0, 20))

    submit_button = Button(
        form_frame,
        text="✨ Apply Changes",
        width=250,
        command=lambda: manage_instance_clicked(action_dropdown, instance_dropdown, manage_window)
    )
    submit_button.pack(pady=30)

def manage_instance_clicked(action_dropdown, instance_dropdown, window):
    action_value = action_dropdown.get()
    instance_value = instance_dropdown.get()

    try:
        runner = CliRunner()
        res = runner.invoke(manage_ec2, [action_value, instance_value])
        if res.exit_code == 0:
            print("Successfully changed the EC2 Instance status")
        else:
            print("Failed to change the EC2 Instance status")

    except Exception as e:
        print(e)

    window.destroy()

def get_instances_for_combobox():
    client = connect("ec2")
    response = client.describe_instances(
        Filters=[
            {"Name": "tag:CreatedBy", "Values": [OWNER]},
            {"Name": "instance-state-name", "Values": ["running", "stopped"]}
        ]
    )

    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_text = f"{instance['InstanceId']}"
            instances.append(instance_text)

    return instances if instances else ["No instances found"]


def open_list_ec2_window():
    list_window, main_frame = create_window("📊 EC2 Instances", "900x700")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "📊 EC2 Instances", 20, "bold")
    title.pack(pady=20)

    table_frame = Frame(main_frame)
    table_frame.pack(fill="both", expand=True, padx=20, pady=20)

    scrollable_frame = ctk.CTkScrollableFrame(table_frame, width=800, height=450)
    scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)
    scrollable_frame.configure(fg_color=COLORS['secondary'])

    headers = ["Name", "Instance ID", "State"]

    for i, header in enumerate(headers):
        header_label = Label(scrollable_frame, header, 16, "bold")
        header_label.configure(
            fg_color=COLORS['accent'],
            corner_radius=10
        )
        header_label.grid(row=0, column=i, padx=10, pady=15, sticky="ew", ipady=10)

    instances = get_list_of_instances()

    for row, instance in enumerate(instances, start=1):
        for col, value in enumerate(instance):
            cell_frame = ctk.CTkFrame(scrollable_frame)
            cell_frame.configure(
                fg_color="transparent",
                corner_radius=8
            )
            cell_frame.grid(row=row, column=col, padx=5, pady=8, sticky="ew")

            cell_label = Label(cell_frame, str(value), 12)
            cell_label.pack(pady=10)

    for i in range(len(headers)):
        scrollable_frame.grid_columnconfigure(i, weight=1)

def get_list_of_instances():
    client = connect("ec2")
    response = client.describe_instances(
        Filters=[
            {"Name": "tag:CreatedBy", "Values": [OWNER]}
        ]
    )

    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_text = f"{instance['InstanceId']}"
            instance_name = next((tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Name"), "N/A")
            instance_state = f"{instance['State']['Name']}"
            instances.append([instance_name, instance_text, instance_state])

    return instances if instances else ["No instances found"]

# S3 functions
def open_create_s3_window():
    create_s3_window, main_frame = create_window("🎯 Create S3 Bucket")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "🎯 Create S3 Bucket", 20, "bold")
    title.pack(pady=20)

    form_frame = Frame(main_frame)
    form_frame.pack(fill="x", padx=20, pady=20)

    visibility_label = Label(form_frame, "🔒 Choose Visibility:", 14, "bold")
    visibility_label.pack(pady=(20, 5))

    visibility_dropdown = ComboBox(
        form_frame,
        values=["public", "private"],
        width=300
    )
    visibility_dropdown.pack(pady=(0, 20))
    visibility_dropdown.set("private")

    submit_button = Button(
        form_frame,
        text="✨ Create Bucket",
        width=250,
        command=lambda: create_s3_clicked(visibility_dropdown, create_s3_window)
    )
    submit_button.configure(
        fg_color=COLORS['success'],
        hover_color="#00b8e6"
    )
    submit_button.pack(pady=30)

def create_s3_clicked(visibility_dropdown, window):
    visibility_value = visibility_dropdown.get()

    user_input = None

    if visibility_value.lower() == "public":
        confirmation = ctk.CTkInputDialog(
            text="Are you sure you want to make this bucket public?\nType 'yes' to confirm:",
            title="Public Bucket Warning"
        )

        user_input = confirmation.get_input()

        if not user_input or user_input.lower() != 'yes':
            print("Bucket creation cancelled by user")
            window.destroy()
            return

    try:
        runner = CliRunner()
        cli_input = 'y\n' if visibility_value.lower() == "public" else None
        result = runner.invoke(create_s3, [visibility_value], input=cli_input)

        output = result.output.strip()

        if "Bucket created:" in output and "Tags added" in output:
            print("S3 Bucket created successfully!")
        elif "Aborted" in output:
            print("Bucket creation cancelled")
        elif "already exists globally" in output:
            print("Bucket name already exists globally")
        elif "Could not make bucket public" in output:
            print("Bucket created as private (public access blocked by AWS)")
        else:
            print(f"Result: {output}")

    except Exception as e:
        print(f"Error: {e}")

    window.destroy()

def open_upload_s3_window():
    upload_window, main_frame = create_window("⬆️ Upload File to S3")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "⬆️ Upload File to S3 Bucket", 20, "bold")
    title.pack(pady=20)

    form_frame = Frame(main_frame)
    form_frame.pack(fill="x", padx=20, pady=20)

    file_path_label = Label(form_frame, "📂 File Path:", 14, "bold")
    file_path_label.pack(pady=(20, 5))

    file_path_entry = Entry(
        form_frame,
        placeholder_text="Enter full file path (e.g., C:/path/to/file.txt)",
        width=400
    )
    file_path_entry.pack(pady=(0, 20))

    buckets = get_buckets_for_combobox()

    buckets_label = Label(form_frame, "🗄️ Choose Bucket:", 14, "bold")
    buckets_label.pack(pady=(20, 5))

    bucket_dropdown = ComboBox(
        form_frame,
        values=buckets,
        width=300
    )
    bucket_dropdown.pack(pady=(0, 20))

    file_name_label = Label(form_frame, "📝 File Name:", 14, "bold")
    file_name_label.pack(pady=(20, 5))

    file_name_entry = Entry(
        form_frame,
        placeholder_text="Enter object name (e.g., my-file.txt)",
        width=400
    )
    file_name_entry.pack(pady=(0, 20))

    submit_button = Button(
        form_frame,
        text="⬆️ Upload File",
        width=250,
        command=lambda: upload_file_clicked(file_path_entry, bucket_dropdown, file_name_entry, upload_window)
    )
    submit_button.pack(pady=30)

def upload_file_clicked(file_path_entry, bucket_dropdown, file_name_entry, window):
    bucket = bucket_dropdown.get()
    file_name = file_name_entry.get()
    file_path = file_path_entry.get()

    if not file_path or not bucket or not file_name:
        print("Please fill all fields")
        return

    if bucket == "No CLI buckets found":
        print("No buckets available")
        return

    try:
        runner = CliRunner()
        result = runner.invoke(upload_file_s3, [file_path, bucket, file_name])

        output = result.output.strip()

        if "The file was uploaded to S3 bucket successfully" in output:
            print("File uploaded to S3 bucket successfully")
        elif "No such file or directory" in output:
            print("File not found at specified path")
        elif "NoSuchBucket" in output:
            print("Bucket does not exist")
        else:
            print(f"Result: {output}")

    except Exception as e:
        print(f"Error: {e}")

    window.destroy()

def open_delete_s3_window():
    delete_window, main_frame = create_window("🗑️ Delete S3 Bucket")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "🗑️ Delete S3 Bucket", 20, "bold")
    title.pack(pady=20)

    form_frame = Frame(main_frame)
    form_frame.pack(fill="x", padx=20, pady=20)

    buckets = get_buckets_for_combobox()

    buckets_label = Label(form_frame, "🗄️ Choose Bucket:", 14, "bold")
    buckets_label.pack(pady=(20, 5))

    bucket_dropdown = ComboBox(
        form_frame,
        values=buckets,
        width=300
    )
    bucket_dropdown.pack(pady=(0, 20))

    submit_button = Button(
        form_frame,
        text="🗑️ Delete Bucket",
        width=250,
        command=lambda: delete_bucket_clicked(bucket_dropdown, delete_window)
    )
    submit_button.configure(
        fg_color=COLORS['error'],
        hover_color="#ff3838"
    )
    submit_button.pack(pady=30)

def get_buckets_for_combobox():
    try:
        s3_client = connect("s3")
        response = s3_client.list_buckets()

        buckets = []
        for bucket in response['Buckets']:
            bucket_name = bucket['Name']
            try:
                tags_response = s3_client.get_bucket_tagging(Bucket=bucket_name)
                tags = {tag['Key']: tag['Value'] for tag in tags_response['TagSet']}

                if tags.get('CreatedBy') == OWNER.lower():
                    buckets.append(bucket_name)
            except ClientError as e:
                continue

        return buckets if buckets else ["No buckets found"]
    except Exception as e:
        return ["No buckets found"]

def delete_bucket_clicked(bucket_dropdown, window):
    bucket_value = bucket_dropdown.get()

    if bucket_value == "No CLI buckets found":
        print("No buckets to delete")
        window.destroy()
        return

    confirmation = ctk.CTkInputDialog(
        text=f"Are you sure you want to delete bucket '{bucket_value}'?\nType 'yes' to confirm:",
        title="Confirm Deletion"
    )

    user_input = confirmation.get_input()

    if user_input and user_input.lower() == 'yes':
        try:
            runner = CliRunner()
            result = runner.invoke(delete_s3, [bucket_value], input='y\n')

            output = result.output.strip()

            if "deleted successfully" in output:
                print("Bucket deleted successfully!")
            else:
                print(f"Result: {output}")

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Deletion cancelled by user")

    window.destroy()

def open_list_s3_window():
    list_window, main_frame = create_window("📋 S3 Buckets", "900x700")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "📋 S3 Buckets", 20, "bold")
    title.pack(pady=20)

    table_frame = Frame(main_frame)
    table_frame.pack(fill="both", expand=True, padx=20, pady=20)

    scrollable_frame = ctk.CTkScrollableFrame(table_frame, width=800, height=450)
    scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)
    scrollable_frame.configure(fg_color=COLORS['secondary'])

    headers = ["Bucket Name", "Visibility", "Created", "Source"]

    for i, header in enumerate(headers):
        header_label = Label(scrollable_frame, header, 16, "bold")
        header_label.configure(
            fg_color=COLORS['accent'],
            corner_radius=10
        )
        header_label.grid(row=0, column=i, padx=10, pady=15, sticky="ew", ipady=10)

    buckets = get_list_of_buckets()

    for row, bucket in enumerate(buckets, start=1):
        for col, value in enumerate(bucket):
            cell_frame = ctk.CTkFrame(scrollable_frame)
            cell_frame.configure(
                fg_color="transparent",
                corner_radius=8
            )
            cell_frame.grid(row=row, column=col, padx=5, pady=8, sticky="ew")

            cell_label = Label(cell_frame, str(value), 12)
            cell_label.pack(pady=10)

    for i in range(len(headers)):
        scrollable_frame.grid_columnconfigure(i, weight=1)

def get_list_of_buckets():
    try:
        s3_client = connect("s3")
        response = s3_client.list_buckets()

        buckets = []
        for bucket in response['Buckets']:
            bucket_name = bucket['Name']
            try:
                tags_response = s3_client.get_bucket_tagging(Bucket=bucket_name)
                tags = {tag['Key']: tag['Value'] for tag in tags_response['TagSet']}

                if tags.get('CreatedBy') == OWNER.lower():
                    buckets.append([
                        bucket_name,
                        tags.get('Visibility', 'N/A'),
                        bucket['CreationDate'].strftime('%Y-%m-%d %H:%M'),
                        "CLI-created"
                    ])
            except ClientError:
                continue

        return buckets if buckets else [["No CLI buckets found", "", "", ""]]

    except Exception as e:
        return [[f"Error: {e}", "", "", ""]]

# Route53 functions
def open_create_route53_window():
    create_route53_window, main_frame = create_window("🎯 Create Route53 Hosted Zone")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "🎯 Create Route53 Hosted Zone", 20, "bold")
    title.pack(pady=20)

    form_frame = Frame(main_frame)
    form_frame.pack(fill="x", padx=20, pady=20)

    zone_name_label = Label(form_frame, "🌐 Domain Name:", 14, "bold")
    zone_name_label.pack(pady=(20, 5))

    zone_name_entry = Entry(
        form_frame,
        placeholder_text="example.com (without www or protocols)",
        width=400
    )
    zone_name_entry.pack(pady=(0, 20))

    validation_label = Label(form_frame, "Enter a valid domain name without protocols", 12)
    validation_label.configure(text_color=COLORS['text_secondary'])
    validation_label.pack(pady=(0, 10))

    submit_button = Button(
        form_frame,
        text="Create Hosted Zone",
        width=250,
        command=lambda: create_route53_clicked(zone_name_entry, create_route53_window)
    )
    submit_button.configure(
        fg_color=COLORS['success'],
        hover_color="#00b8e6"
    )
    submit_button.pack(pady=30)

def create_route53_clicked(zone_name_entry, window):
    zone_name_value = zone_name_entry.get()

    if not zone_name_value:
        print("Please enter a domain name")
        return
    elif zone_name_value.startswith(("http://", "https://", "www.")):
        print("Remove protocols and www prefix")
        return
    elif " " in zone_name_value or not "." in zone_name_value:
        print("Invalid domain format")
        return

    try:
        runner = CliRunner()
        result = runner.invoke(create_route53, [zone_name_value])

        output = result.output.strip()

        if "Created hosted zone:" in output and "Tags added" in output:
            print("Hosted zone created successfully!")
        elif "Aborted" in output:
            print("Hosted zone creation cancelled")
        elif "already exists globally" in output:
            print("Hosted zone already exists globally")
        else:
            print(f"Result: {output}")

    except Exception as e:
        print(f"Error: {e}")

    window.destroy()

def open_manage_route53_window():
    manage_window, main_frame = create_window("⚙️ Manage Route53")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "⚙️ Manage Route53 Hosted Zone", 20, "bold")
    title.pack(pady=20)

    button_container = Frame(main_frame)
    button_container.pack(fill="x", padx=20, pady=20)

    record_create_btn = Button(
        button_container,
        text="🎯 Create Record",
        width=300,
        command=lambda: [manage_window.destroy(), open_create_record_window()]
    )
    record_create_btn.pack(pady=15)

    record_update_btn = Button(
        button_container,
        text="⚙️ Update Record",
        width=300,
        command=lambda: [manage_window.destroy(), open_update_record_window()]
    )
    record_update_btn.pack(pady=15)

    record_delete_btn = Button(
        button_container,
        text="🗑️ Delete Record",
        width=300,
        command=lambda: [manage_window.destroy(), open_delete_record_window()]
    )
    record_delete_btn.pack(pady=15)

def open_create_record_window():
    create_record_window, main_frame = create_window("🎯 Create Record")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "🎯 Create New Record", 20, "bold")
    title.pack(pady=20)

    form_frame = Frame(main_frame)
    form_frame.pack(fill="x", padx=20, pady=20)

    record_name_label = Label(form_frame, "Record Name:", 14, "bold")
    record_name_label.pack(pady=(20, 5))

    record_name_entry = Entry(
        form_frame,
        placeholder_text="Enter a record name (e.g, www.example.com)",
        width=400
    )
    record_name_entry.pack(pady=(0, 20))

    hosted_zones = get_hosted_zones_for_combobox()

    hosted_zones_label = Label(form_frame, "Choose Hosted Zone:", 14, "bold")
    hosted_zones_label.pack(pady=(20, 5))

    hosted_zones_dropdown = ComboBox(
        form_frame,
        values=hosted_zones,
        width=300
    )
    hosted_zones_dropdown.pack(pady=(0, 20))

    record_type_label = Label(form_frame, "Record Type:", 14, "bold")
    record_type_label.pack(pady=(20, 5))

    record_type_dropdown = ComboBox(
        form_frame,
        values=["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SOA"],
        width=300
    )
    record_type_dropdown.pack(pady=(0, 20))
    record_type_dropdown.set("A")

    record_value_label = Label(form_frame, "Record Value:", 14, "bold")
    record_value_label.pack(pady=(20, 5))

    record_value_entry = Entry(
        form_frame,
        placeholder_text="Enter a record Value (e.g, 1.2.3.4)",
        width=400
    )
    record_value_entry.pack(pady=(0, 20))

    submit_button = Button(
        form_frame,
        text="✨ Create Record",
        width=250,
        command=lambda: create_record_clicked(record_name_entry, hosted_zones_dropdown, record_type_dropdown,
                                              record_value_entry, create_record_window)
    )
    submit_button.configure(
        fg_color=COLORS['success'],
        hover_color="#00b8e6"
    )
    submit_button.pack(pady=30)

def get_records_for_zone(zone_name):
    try:
        client = connect("route53")

        response = client.list_hosted_zones()['HostedZones']
        zone_id = None

        for zone in response:
            if zone['Name'] == zone_name:
                zone_id = zone['Id'].split('/')[-1]
                break

        if not zone_id:
            return []

        records_response = client.list_resource_record_sets(HostedZoneId=zone_id)
        records = []

        for record in records_response['ResourceRecordSets']:
            if record['Type'] in ['NS', 'SOA'] and record['Name'] == zone_name:
                continue

            record_values = []
            if 'ResourceRecords' in record:
                record_values = [rr['Value'] for rr in record['ResourceRecords']]
            elif 'AliasTarget' in record:
                record_values = [record['AliasTarget']['DNSName']]

            records.append({
                'name': record['Name'],
                'type': record['Type'],
                'values': record_values,
                'ttl': record.get('TTL', 'N/A')
            })

        return records

    except Exception as e:
        print(f"Error getting records: {e}")
        return []

def open_update_record_window():
    update_window, main_frame = create_window("⚙️ Update Record")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "⚙️ Update DNS Record", 20, "bold")
    title.pack(pady=20)

    form_frame = Frame(main_frame)
    form_frame.pack(fill="x", padx=20, pady=20)

    hosted_zones = get_hosted_zones_for_combobox()

    hosted_zones_label = Label(form_frame, "Choose Hosted Zone:", 14, "bold")
    hosted_zones_label.pack(pady=(20, 5))

    hosted_zones_dropdown = ComboBox(
        form_frame,
        values=hosted_zones,
        width=300
    )
    hosted_zones_dropdown.pack(pady=(0, 20))

    records_label = Label(form_frame, "Choose Record:", 14, "bold")
    records_label.pack(pady=(20, 5))

    records_dropdown = ComboBox(
        form_frame,
        values=["Select hosted zone first"],
        width=400
    )
    records_dropdown.pack(pady=(0, 20))

    new_value_label = Label(form_frame, "New Value:", 14, "bold")
    new_value_label.pack(pady=(20, 5))

    new_value_entry = Entry(
        form_frame,
        placeholder_text="Enter new record value",
        width=400
    )
    new_value_entry.pack(pady=(0, 20))

    def on_zone_change():
        selected_zone = hosted_zones_dropdown.get()
        if selected_zone and selected_zone != "No hosted zones found":
            records = get_records_for_zone(selected_zone)
            if records:
                record_options = []
                for record in records:
                    values_str = ", ".join(record['values'][:2])
                    if len(record['values']) > 2:
                        values_str += "..."
                    record_display = f"{record['name']} ({record['type']}) → {values_str}"
                    record_options.append(record_display)

                records_dropdown.configure(values=record_options)
                records_dropdown.set("Select a record")
            else:
                records_dropdown.configure(values=["No records found"])
                records_dropdown.set("No records found")

    hosted_zones_dropdown.configure(command=lambda x: on_zone_change())

    submit_button = Button(
        form_frame,
        text="✨ Update Record",
        width=250,
        command=lambda: update_record_clicked(hosted_zones_dropdown, records_dropdown, new_value_entry, update_window)
    )
    submit_button.configure(
        fg_color=COLORS['warning'],
        hover_color="#ff8c42"
    )
    submit_button.pack(pady=30)

def open_delete_record_window():
    delete_window, main_frame = create_window("🗑️ Delete Record")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "Delete DNS Record", 20, "bold")
    title.pack(pady=20)

    form_frame = Frame(main_frame)
    form_frame.pack(fill="x", padx=20, pady=20)

    hosted_zones = get_hosted_zones_for_combobox()

    hosted_zones_label = Label(form_frame, "Choose Hosted Zone:", 14, "bold")
    hosted_zones_label.pack(pady=(20, 5))

    hosted_zones_dropdown = ComboBox(
        form_frame,
        values=hosted_zones,
        width=300
    )
    hosted_zones_dropdown.pack(pady=(0, 20))

    records_label = Label(form_frame, "Choose Record to Delete:", 14, "bold")
    records_label.pack(pady=(20, 5))

    records_dropdown = ComboBox(
        form_frame,
        values=["Select hosted zone first"],
        width=500
    )
    records_dropdown.pack(pady=(0, 20))

    def on_zone_change_delete():
        selected_zone = hosted_zones_dropdown.get()
        if selected_zone and selected_zone != "No hosted zones found":
            records = get_records_for_zone(selected_zone)
            if records:
                record_options = []
                for record in records:
                    values_str = ", ".join(record['values'])
                    record_display = f"{record['name']} | {record['type']} | {values_str} | TTL: {record['ttl']}"
                    record_options.append(record_display)

                records_dropdown.configure(values=record_options)
                records_dropdown.set("Select a record to delete")
            else:
                records_dropdown.configure(values=["No records found"])
                records_dropdown.set("No records found")

    hosted_zones_dropdown.configure(command=lambda x: on_zone_change_delete())

    warning_label = Label(form_frame, "Warning: This action cannot be undone!", 12)
    warning_label.configure(text_color=COLORS['error'])
    warning_label.pack(pady=(10, 20))

    submit_button = Button(
        form_frame,
        text="🗑️ Delete Record",
        width=250,
        command=lambda: delete_record_clicked(hosted_zones_dropdown, records_dropdown, delete_window)
    )
    submit_button.configure(
        fg_color=COLORS['error'],
        hover_color="#ff3838"
    )
    submit_button.pack(pady=30)


def create_record_clicked(name_entry, zone_dropdown, type_dropdown, value_entry, window):
    record_name = name_entry.get().strip()
    zone_name = zone_dropdown.get()
    record_type = type_dropdown.get()
    record_value = value_entry.get().strip()

    if not all([record_name, zone_name, record_type, record_value]):
        print("Please fill all fields")
        return

    if zone_name == "No hosted zones found":
        print("No hosted zone selected")
        return

    try:
        client = connect("route53")
        response = client.list_hosted_zones()['HostedZones']
        zone_id = None

        for zone in response:
            if zone['Name'] == zone_name:
                zone_id = zone['Id'].split('/')[-1]
                break

        if not zone_id:
            print("Could not find zone ID")
            return

        runner = CliRunner()
        result = runner.invoke(manage_route53, ['create', zone_id, record_name, record_type, record_value])

        output = result.output.strip()

        if "Record created successfully" in output:
            print("Record created successfully!")
        else:
            print(f"Result: {output}")

    except Exception as e:
        print(f"Error: {e}")

    window.destroy()

def update_record_clicked(zone_dropdown, record_dropdown, value_entry, window):
    zone_name = zone_dropdown.get()
    selected_record = record_dropdown.get()
    new_value = value_entry.get().strip()

    if not all([zone_name, selected_record, new_value]) or selected_record in ["Select hosted zone first",
                                                                               "Select a record", "No records found"]:
        print("Please fill all fields")
        return

    try:
        record_name = selected_record.split(" (")[0]
        record_type = selected_record.split("(")[1].split(")")[0]

        zone_id = get_zone_id_by_name(zone_name)
        if not zone_id:
            print("Could not find zone ID")
            return

        runner = CliRunner()
        result = runner.invoke(manage_route53, ['update', zone_id, record_name, record_type, new_value])

        output = result.output.strip()

        if "OK:" in output and "UPSERT" in output:
            print("Record updated successfully!")
        else:
            print(f"Result: {output}")

    except Exception as e:
        print(f"Error: {e}")

    window.destroy()


def delete_record_clicked(zone_dropdown, record_dropdown, window):
    zone_name = zone_dropdown.get()
    selected_record = record_dropdown.get()

    if not all([zone_name, selected_record]) or selected_record in ["Select hosted zone first",
                                                                    "Select a record to delete", "No records found"]:
        print("Please select a record to delete")
        return

    confirmation = ctk.CTkInputDialog(
        text=f"Are you sure you want to delete this record?\n{selected_record}\n\nType 'DELETE' to confirm:",
        title="Confirm Deletion"
    )

    user_input = confirmation.get_input()

    if user_input != "DELETE":
        print("Deletion cancelled")
        window.destroy()
        return

    try:
        parts = selected_record.split(" | ")
        record_name = parts[0]
        record_type = parts[1]
        record_value = parts[2].split(",")[0].strip()

        zone_id = get_zone_id_by_name(zone_name)
        if not zone_id:
            print("Could not find zone ID")
            return

        runner = CliRunner()
        result = runner.invoke(manage_route53, ['delete', zone_id, record_name, record_type, record_value])

        output = result.output.strip()

        if "OK:" in output and "DELETE" in output:
            print("Record deleted successfully!")
        else:
            print(f"Result: {output}")

    except Exception as e:
        print(f"Error: {e}")

    window.destroy()

def get_zone_id_by_name(zone_name):
    try:
        client = connect("route53")
        response = client.list_hosted_zones()['HostedZones']

        for zone in response:
            if zone['Name'] == zone_name:
                return zone['Id'].split('/')[-1]

        return None

    except Exception as e:
        print(f"Error finding zone ID: {e}")
        return None

def get_hosted_zones_for_combobox():
    try:
        client = connect("route53")
        response = client.list_hosted_zones()['HostedZones']

        zones = []
        for zone in response:
            zone_id = zone['Id'].split('/')[-1]
            zone_name = zone['Name']
            try:
                tags_res = client.list_tags_for_resource(ResourceType="hostedzone", ResourceId=zone_id)
                tags = {t["Key"]: t["Value"] for t in tags_res["ResourceTagSet"]["Tags"]}

                if tags.get('CreatedBy') == OWNER.lower():
                    zones.append(zone_name)
            except ClientError:
                continue

        return zones if zones else ["No hosted zones found"]

    except Exception as e:
        print(f"Error: {e}")
        return ["No hosted zones found"]

def open_list_route53_window():
    list_window, main_frame = create_window("📋 Hosted Zones List", "800x600")

    header = GlowEffect(main_frame)
    header.pack(fill="x", pady=(0, 30))

    title = Label(header, "📋 My Hosted Zones", 20, "bold")
    title.pack(pady=20)

    table_frame = Frame(main_frame)
    table_frame.pack(fill="both", expand=True, padx=20, pady=20)

    scrollable_frame = ctk.CTkScrollableFrame(table_frame, width=750, height=400)
    scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)
    scrollable_frame.configure(fg_color=COLORS['secondary'])

    headers = ["Zone Name", "Zone ID", "Record Count", "Status"]

    for i, header in enumerate(headers):
        header_label = Label(scrollable_frame, header, 14, "bold")
        header_label.configure(
            fg_color=COLORS['accent'],
            corner_radius=10
        )
        header_label.grid(row=0, column=i, padx=10, pady=15, sticky="ew", ipady=10)

    try:
        client = connect("route53")
        zones_response = client.list_hosted_zones()['HostedZones']

        row = 1
        for zone in zones_response:
            zone_id = zone['Id'].split('/')[-1]
            zone_name = zone['Name']

            try:
                tags_res = client.list_tags_for_resource(ResourceType="hostedzone", ResourceId=zone_id)
                tags = {t["Key"]: t["Value"] for t in tags_res["ResourceTagSet"]["Tags"]}

                if tags.get('CreatedBy') == OWNER.lower():
                    try:
                        records_response = client.list_resource_record_sets(HostedZoneId=zone_id)
                        record_count = len(records_response['ResourceRecordSets'])
                    except:
                        record_count = "N/A"

                    zone_data = [zone_name, zone_id, str(record_count), "Active"]

                    for col, value in enumerate(zone_data):
                        cell_frame = ctk.CTkFrame(scrollable_frame)
                        cell_frame.configure(
                            fg_color="transparent",
                            corner_radius=8
                        )
                        cell_frame.grid(row=row, column=col, padx=5, pady=8, sticky="ew")

                        cell_label = Label(cell_frame, str(value), 12)
                        if col == 3:
                            cell_label.configure(text_color=COLORS['success'])
                        cell_label.pack(pady=10)

                    row += 1

            except ClientError:
                continue

        if row == 1:
            no_zones_label = Label(scrollable_frame, "No hosted zones found", 16)
            no_zones_label.grid(row=1, column=0, columnspan=4, pady=50)

    except Exception as e:
        error_label = Label(scrollable_frame, f"Error: {e}", 16)
        error_label.configure(text_color=COLORS['error'])
        error_label.grid(row=1, column=0, columnspan=4, pady=50)

    for i in range(len(headers)):
        scrollable_frame.grid_columnconfigure(i, weight=1)


setup_ec2_tab()
setup_s3_tab()
setup_route53_tab()

status_bar = Frame(main_container)
status_bar.pack(fill="x", padx=20, pady=(0, 20))

status_label = Label(status_bar, "🟢 AWS Resource Manager", 12)
status_label.configure(text_color=COLORS['success'])
status_label.pack(pady=10)

root.mainloop()