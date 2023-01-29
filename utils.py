from pprint import pprint # pretty print
import requests # for making HTTP requests
import matplotlib.pyplot as plt # for plotting
from PIL import Image # for image manipulation
import textwrap # for wrapping text 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 


def wolframAlpha_report(report_json : dict) -> str:
    """ Get the report from WolframAlpha
    Args:
        r (dict): The response from WolframAlpha
    Returns:
        str: The report from WolframAlpha
    """
    # Check the format of the response
    if report_json["queryresult"]["success"] == "false":
        return "Sorry, the query failed."
    elif report_json["queryresult"]["success"] == "true":
        pass
    # Get the pods, the pods are the different answers
    # (A Pod is a grouping of one or more containers that operate together.)
    pods = report_json["queryresult"]["pods"]
    # String to store the report
    report = ""
    for pod in pods:
        # Add the title of the pod to the report
        report += pod["title"] + " "
        imgs = []
        if "result"  or "plot" in pod["title"].lower():
            for subpod in pod["subpods"]:
                data = subpod
                # If plaintext is in the subpod
                if "plaintext" in data:
                    report += data["plaintext"] + " "
                # If img is in the subpod
                if "img" in data:
                    if "plot" in data["img"]["type"].lower():
                        imgs.append(data["img"]["src"])
                # If mathml is in the subpod
                if "mathml" in data:
                    report += data["mathml"] + " "
                # If datasources is in the subpod
                if "datasources" in data:
                    # If there are more than one datasources
                    if len(data["datasources"]) > 1:
                        report += ", ".join(data["datasources"]["datasource"]) + " "
                    else:
                        report += data["datasources"]["datasource"] + " "
                # If microsources is in the subpod
                if "microsources" in data:
                    if len(data["microsources"]) > 1:
                        report += ", ".join(data["microsources"]["microsource"]) + " "
                    else:
                        report += data["microsources"]["microsource"]
        else:
            # print the subpods
            last_line = False
            last_subpod = False
            # Print the plaintext of each subpod
            for subpod in pod["subpods"]:
                if subpod == pod["subpods"][-1]:
                    last_subpod = True
                lines = subpod["plaintext"].split("\n")
                # If it is the first line, continue printing. otherwise, print a new line
                for line in lines:
                    if line == lines[-1]:
                        last_line = True
                    report += ", {}".format(line)
                    # if the end
                    if last_line and last_subpod:
                        report += " "
    # If images are found, download them and show them
    imgs_files = []
    if imgs:
        for i, img in enumerate(imgs):
            # Download the image
            img_data = requests.get(img).content
            with open('img_{}.png'.format(i), 'wb') as handler:
                handler.write(img_data)
                handler.close()
                # Open the image and save it as png
                im = Image.open('img_{}.png'.format(i))
                im.save('img_{}.png'.format(i))
                imgs_files.append('img_{}.png'.format(i))
    # Return the report
    return {"report": report, "imgs_files": imgs_files}
    
    
def show_text_and_image(text : str, imgs : list):
    """ Show the text and the image
    Args:
        text (str): The text to show
        img_name (str): The name of the image to show
    """

    # Get the number of lines
    lines = textwrap.wrap(text, 80)
    # Inset a new line every 80 characters
    text = "\n".join(lines)
    
    if imgs:
        # There are images
        # Show the text on the left and the image on the right
        _, ax = plt.subplots(1, 2, figsize=(30, 10))
        # Show the text on the left
        ax[0].text(0, 0, text, fontsize=20)
        ax[0].axis('off')

        # Show the image on the right
        img = mpimg.imread(imgs[0])
        ax[1].imshow(img)
        ax[1].axis('off')
    else:
        # There are no images
        # Show the text
        _, ax = plt.subplots(1, 1, figsize=(10, 10))
        ax.text(0, 0, text, fontsize=20)
        ax.axis('off')
        
    plt.show()
