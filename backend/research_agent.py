"""
AI Research Agent for Account Intelligence

Uses Groq API to analyze visitor signals and generate
account intelligence including intent scores, persona inference,
and sales recommendations.
"""
import os
import json
import logging
from groq import Groq
from groq import APIError

# Configure module-level logging
logger = logging.getLogger(__name__)

# Environment variables
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_MODEL = os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile')


class GroqAPIError(Exception):
    """Custom exception for Groq API errors"""
    pass


def verify_api_configuration():
    """
    Verify that Groq API is properly configured.

    Raises:
        ValueError: If GROQ_API_KEY is not set
    """
    if not GROQ_API_KEY:
        raise ValueError('GROQ_API_KEY environment variable not set. '
                        'Please configure this in GitHub Secrets or your .env file.')

    logger.info(f"✅ Groq API configured (model: {GROQ_MODEL})")


def create_prompt(company_name, pages):
    """
    Create the AI prompt for account intelligence analysis.

    Args:
        company_name: Name of the company to analyze
        pages: List of pages visited

    Returns:
        str: The formatted prompt
    """
    pages_str = ', '.join(pages) if pages else 'No pages visited'

    return f"""
Analyze {company_name} based on visits to: {pages_str}.

SCORING RUBRIC (Strict):
- 10: Visited BOTH /pricing AND /demo-request.
- 7-9: Visited /docs or multiple /case-studies.
- 4-6: Visited /about-us or 2+ /blog posts.
- 1-3: Only 1 /blog post or just /home.

Return ONLY a JSON object:
{{
    "industry": "string", "company_size": "string", "hq": "string",
    "website": "string", "persona_inference": "string",
    "intent_score": (int 1-10), "intent_stage": "string",
    "confidence_score": (int 1-100),
    "ai_summary": "2 sentences", "sales_action": "1 specific step",
    "tech_stack": "list", "leadership": "names",
    "business_signals": "news", "sales_hook": "one-liner",
    "key_signals_observed": "summary of behavior"
}}
"""


def get_account_intel(company_name, pages):
    """
    Get account intelligence from Groq AI.

    Args:
        company_name: Name of the company to analyze
        pages: List of pages visited by the company

    Returns:
        dict: Account intelligence data

    Raises:
        ValueError: If API key is not configured
        GroqAPIError: If the API call fails
    """
    # Verify configuration
    verify_api_configuration()

    # Initialize client
    client = Groq(api_key=GROQ_API_KEY)

    # Create prompt
    prompt = create_prompt(company_name, pages)

    logger.debug(f"🔍 Analyzing {company_name} with {len(pages) if pages else 0} pages")

    try:
        # Call Groq API
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a Revenue Analyst. Return ONLY JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=GROQ_MODEL,
            response_format={"type": "json_object"}
        )

        # Parse response
        content = response.choices[0].message.content
        result = json.loads(content)

        # Validate required fields
        required_fields = ['industry', 'company_size', 'hq', 'website',
                          'persona_inference', 'intent_score', 'intent_stage',
                          'confidence_score', 'ai_summary', 'sales_action',
                          'tech_stack', 'leadership', 'business_signals',
                          'sales_hook', 'key_signals_observed']

        missing_fields = [f for f in required_fields if f not in result]
        if missing_fields:
            logger.warning(f"⚠️ Missing fields in response: {missing_fields}")

        logger.info(f"✅ Analysis complete for {company_name} "
                   f"(Intent: {result.get('intent_score', 'N/A')}/10, "
                   f"Confidence: {result.get('confidence_score', 'N/A')}%)")

        return result

    except json.JSONDecodeError as e:
        raise GroqAPIError(f"Failed to parse AI response as JSON: {e}")

    except APIError as e:
        # Handle Groq-specific errors
        error_msg = str(e)

        if 'authentication' in error_msg.lower():
            raise GroqAPIError("Invalid Groq API key. Please check GROQ_API_KEY.")
        elif 'rate limit' in error_msg.lower():
            raise GroqAPIError("Groq API rate limit exceeded. Please try again later.")
        elif 'timeout' in error_msg.lower():
            raise GroqAPIError("Groq API request timed out.")
        else:
            raise GroqAPIError(f"Groq API error: {error_msg}")

    except Exception as e:
        raise GroqAPIError(f"Unexpected error during AI analysis: {e}")


# Test function for development
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    test_company = "Acme Corporation"
    test_pages = ["/pricing", "/demo-request", "/about-us"]

    try:
        result = get_account_intel(test_company, test_pages)
        print(json.dumps(result, indent=2))
    except (ValueError, GroqAPIError) as e:
        print(f"❌ Error: {e}")
