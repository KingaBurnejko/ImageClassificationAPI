import os
import csv

def generate_labels_csv(root_dir, output_file="data/labels.csv"):
    data = []
    for class_name in sorted(os.listdir(root_dir)):
        class_path = os.path.join(root_dir, class_name)
        if os.path.isdir(class_path):
            for img_file in os.listdir(class_path):
                if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                    data.append((os.path.join(class_name, img_file), class_name))

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "label"])
        writer.writerows(data)

    return output_file
