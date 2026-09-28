from PIL import Image, ImageStat, ImageFilter
import os


def analyze_image(file_path: str):
    """
    Perform basic image forensic analysis.

    These results are forensic indicators only.
    They do not prove that an image is real or AI-generated.
    """

    try:
        image = Image.open(file_path)

        width, height = image.size
        image_format = image.format or "Unknown"
        color_mode = image.mode or "Unknown"

        file_size_kb = os.path.getsize(file_path) / 1024

        # -------------------------------------
        # METADATA
        # -------------------------------------

        metadata = {}

        for key, value in image.getexif().items():
            metadata[str(key)] = str(value)

        # -------------------------------------
        # BRIGHTNESS ANALYSIS
        # -------------------------------------

        grayscale = image.convert("L")

        brightness = ImageStat.Stat(
            grayscale
        ).mean[0]

        if brightness < 60:
            brightness_status = "Dark image"
        elif brightness > 200:
            brightness_status = "Bright image"
        else:
            brightness_status = "Normal brightness"

        # -------------------------------------
        # NOISE ESTIMATION
        # -------------------------------------

        blurred = grayscale.filter(
            ImageFilter.GaussianBlur(radius=1)
        )

        difference = ImageStat.Stat(
            Image.blend(
                grayscale,
                blurred,
                0.5
            )
        ).mean[0]

        noise_estimate = round(
            abs(
                ImageStat.Stat(grayscale).mean[0]
                -
                ImageStat.Stat(blurred).mean[0]
            ),
            2
        )

        if noise_estimate < 2:
            noise_status = "Low estimated variation"
        elif noise_estimate < 8:
            noise_status = "Moderate estimated variation"
        else:
            noise_status = "Higher estimated variation"

        # -------------------------------------
        # EDGE ANALYSIS
        # -------------------------------------

        edges = grayscale.filter(
            ImageFilter.FIND_EDGES
        )

        edge_mean = ImageStat.Stat(
            edges
        ).mean[0]

        edge_density = round(
            edge_mean,
            2
        )

        if edge_density < 10:
            edge_status = "Low edge activity"
        elif edge_density < 30:
            edge_status = "Moderate edge activity"
        else:
            edge_status = "High edge activity"

        # -------------------------------------
        # FORENSIC INDICATORS
        # -------------------------------------

        indicators = [
            {
                "name": "Metadata",
                "result": (
                    "Metadata present"
                    if metadata
                    else "No EXIF metadata found"
                )
            },
            {
                "name": "Brightness",
                "result": (
                    f"{brightness:.2f} — "
                    f"{brightness_status}"
                )
            },
            {
                "name": "Noise Estimate",
                "result": (
                    f"{noise_estimate} — "
                    f"{noise_status}"
                )
            },
            {
                "name": "Edge Activity",
                "result": (
                    f"{edge_density} — "
                    f"{edge_status}"
                )
            },
            {
                "name": "Image Format",
                "result": image_format
            },
            {
                "name": "Dimensions",
                "result": (
                    f"{width} × {height}px"
                )
            },
            {
                "name": "Color Mode",
                "result": color_mode
            },
            {
                "name": "File Size",
                "result": (
                    f"{file_size_kb:.2f} KB"
                )
            }
        ]

        return {
            "success": True,
            "width": width,
            "height": height,
            "format": image_format,
            "color_mode": color_mode,
            "file_size_kb": round(
                file_size_kb,
                2
            ),
            "metadata": metadata,
            "brightness": round(
                brightness,
                2
            ),
            "noise_estimate": noise_estimate,
            "edge_density": edge_density,
            "indicators": indicators,
            "warning": (
                "These forensic indicators are "
                "heuristic signals. They do not prove "
                "whether an image is authentic, edited, "
                "or AI-generated."
            )
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }