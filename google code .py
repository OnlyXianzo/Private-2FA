import base64
import urllib.parse
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

# Your full URL pasted here
encoded_url = '''YOUR_MIGRATION_URL_HERE'''  # Replace this with your actual migration URL

# Step 1: Extract base64
b64_data = urllib.parse.unquote(encoded_url.split("data=")[1])
binary_data = base64.b64decode(b64_data)

# Step 2: Dynamically define protobuf schema
pool = descriptor_pool.Default()
file_desc_proto = descriptor_pb2.FileDescriptorProto()
file_desc_proto.name = "migration.proto"
file_desc_proto.package = "migration"

# OTPParameters message
file_desc_proto.message_type.add(
    name="OTPParameters",
    field=[
        descriptor_pb2.FieldDescriptorProto(name="secret", number=1, type=12),
        descriptor_pb2.FieldDescriptorProto(name="name", number=2, type=9),
        descriptor_pb2.FieldDescriptorProto(name="issuer", number=3, type=9),
        descriptor_pb2.FieldDescriptorProto(name="algorithm", number=4, type=5),
        descriptor_pb2.FieldDescriptorProto(name="digits", number=5, type=5),
        descriptor_pb2.FieldDescriptorProto(name="type", number=6, type=5),
    ]
)

# MigrationPayload message
file_desc_proto.message_type.add(
    name="MigrationPayload",
    field=[
        descriptor_pb2.FieldDescriptorProto(name="otp_parameters", number=1, label=3, type=11, type_name=".migration.OTPParameters"),
        descriptor_pb2.FieldDescriptorProto(name="version", number=2, type=5),
        descriptor_pb2.FieldDescriptorProto(name="batch_size", number=3, type=5),
        descriptor_pb2.FieldDescriptorProto(name="batch_index", number=4, type=5),
        descriptor_pb2.FieldDescriptorProto(name="batch_id", number=5, type=5),
    ]
)

# Register
file_desc = pool.Add(file_desc_proto)
messages = message_factory.GetMessages([file_desc_proto])
Payload = messages["migration.MigrationPayload"]
OTPEntry = messages["migration.OTPParameters"]

# Step 3: Parse
payload = Payload.FromString(binary_data)


# Step 4: Output secrets
for entry in payload.otp_parameters:
    secret = base64.b32encode(entry.secret).decode().replace('=', '')
    print(f"🔐 Account: {entry.name}")
    print(f"📧 Issuer: {entry.issuer}")
    print(f"🔑 Secret: {secret}")
    print("------")


#     Step to use       #
#  Step 1: Export code form your autheticator (eg. Google Autheticator)
#  Step 2: Scan QR with Google Lens or any ohher QR scanner 
#  Step 3: Copy the text(address) shown after scanning the QR 
#  Step 4: Paste this at line Encoded_url is a format like encoded_url = '''Your link(without space)'''
#  Step 5: In the terminal you will see all Account, issuer name, and Secret key
#   DON'T FORGET TO FOLLOW ME ON GITHUB AND IF YOU FACE ANY ISSUE JUST COMMENT 