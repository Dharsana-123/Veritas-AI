import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

from factcheck.source_quality import assess_source_quality
load_dotenv()

TAVILY_API_URL = "https://api.tavily.com/search"


def retrieve_evidence(claim: str) -> List[Dict]:
    claim = claim.strip()

    if not claim:
        return []

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return [
            {
                "title": "Search configuration error",
                "source": "Tavily",
                "url": None,
                "snippet": "TAVILY_API_KEY was not found."
            }
        ]

    try:
        response = requests.post(
            TAVILY_API_URL,
            json={
                "api_key": api_key,
                "query": claim,
                "search_depth": "advanced",
                "max_results": 5,
                "include_answer": False
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get("results", []):
            url = item.get("url")

            quality_info = assess_source_quality(url)

            results.append(
             {
               "title": item.get("title"),
               "source": url,
               "url": url,
               "snippet": item.get("content"),

               "quality": quality_info["quality"],
               "quality_reason": quality_info["reason"],
               "source_type": quality_info["source_type"]
             }
            ) 

        return results

    except requests.RequestException as error:
        return [
            {
                "title": "Evidence retrieval failed",
                "source": "Web search",
                "url": None,
                "snippet": str(error)
            }
        ]