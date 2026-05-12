import type { APIRoute } from "astro";

// Mark this endpoint as dynamic (server-rendered) not static
export const prerender = false;

const API_TOKEN = import.meta.env.API_TOKEN || "";
const BACKEND_URL = import.meta.env.PUBLIC_API_BASE_URL || "http://localhost:8000";

export const POST: APIRoute = async ({ request }) => {
  try {
    // Check if the request has a body
    const contentType = request.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      return new Response(
        JSON.stringify({ detail: "Content-Type must be application/json" }),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        }
      );
    }

    // Parse the request body
    let payload;
    try {
      const text = await request.text();
      if (!text) {
        return new Response(
          JSON.stringify({ detail: "Request body cannot be empty" }),
          {
            status: 400,
            headers: { "Content-Type": "application/json" },
          }
        );
      }
      payload = JSON.parse(text);
    } catch (parseError) {
      return new Response(JSON.stringify({ detail: "Invalid JSON in request body" }), {
        status: 400,
        headers: { "Content-Type": "application/json" },
      });
    }

    // Call the backend with the bearer token
    const backendResponse = await fetch(`${BACKEND_URL}/api/validate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${API_TOKEN}`,
      },
      body: JSON.stringify(payload),
    });

    // Get the response text first
    const responseText = await backendResponse.text();
    let data;
    
    try {
      data = JSON.parse(responseText);
    } catch {
      // If backend response is not JSON (e.g., HTML error page), return a generic error
      console.error("Backend returned non-JSON response:", responseText);
      return new Response(
        JSON.stringify({ detail: "Backend error: invalid response format" }),
        {
          status: backendResponse.status || 500,
          headers: { "Content-Type": "application/json" },
        }
      );
    }

    // Return the response with the same status code
    return new Response(JSON.stringify(data), {
      status: backendResponse.status,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("Backend request failed:", error);
    return new Response(
      JSON.stringify({ detail: "Internal server error" }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
};
