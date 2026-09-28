from urllib.parse import urlparse


def assess_source_quality(url: str):
    """
    Simple heuristic-based source quality assessment.

    This is an indicator, not a definitive measure
    of whether a source is trustworthy.
    """

    if not url:
        return {
            "quality": "Unknown",
            "reason": "No source URL available.",
            "source_type": "Unknown"
        }

    try:
        domain = urlparse(url).netloc.lower()

        # Remove www.
        domain = domain.replace("www.", "")

        # Official / institutional sources
        if (
            domain.endswith(".gov")
            or domain.endswith(".gov.in")
            or domain.endswith(".edu")
            or domain.endswith(".edu.in")
            or domain.endswith(".ac.in")
        ):
            return {
                "quality": "High",
                "reason": "Government or educational/institutional domain.",
                "source_type": "Institutional"
            }

        # Known reference/scientific organizations
        trusted_domains = [
            "britannica.com",
            "nasa.gov",
            "who.int",
            "un.org",
            "nature.com",
            "sciencedirect.com"
        ]

        if any(domain == d or domain.endswith("." + d)
               for d in trusted_domains):
            return {
                "quality": "High",
                "reason": "Recognized reference or scientific organization.",
                "source_type": "Reference / Scientific"
            }

        # Social platforms
        social_domains = [
            "facebook.com",
            "instagram.com",
            "x.com",
            "twitter.com",
            "tiktok.com",
            "youtube.com"
        ]

        if any(domain == d or domain.endswith("." + d)
               for d in social_domains):
            return {
                "quality": "Low",
                "reason": "User-generated or social-media content requires independent corroboration.",
                "source_type": "Social Media"
            }

        # General web source
        return {
            "quality": "Medium",
            "reason": "General web source; independent corroboration may be useful.",
            "source_type": "General Web"
        }

    except Exception:
        return {
            "quality": "Unknown",
            "reason": "Unable to classify the source.",
            "source_type": "Unknown"
        }