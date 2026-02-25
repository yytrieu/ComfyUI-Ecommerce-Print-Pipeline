# ComfyUI AI Print Pipeline
### Automated E-Commerce Workflow for Shirt Color Swapping & Design Inpainting

This repository contains a high-end **ComfyUI Workflow** designed to automate the production of T-shirt mockups. The pipeline solves two major industry challenges: precise color adjustment of the base garment and the seamless integration of digital prints into fabric textures using the **Flux Fill** architecture.

---

## 🚀 Technical Highlights

* **ShirtColorSwapper (Custom Node):** A dedicated logic block that takes a white mockup and a garment mask to perform high-fidelity color swaps via Hex codes while preserving shadows and highlights.
* **Flux Fill Inpainting:** Utilizes the `flux1-fill-dev` model for superior inpainting, ensuring that the design follows the natural folds, wrinkles, and weave of the fabric.
* **Global Signal Broadcasting:** Implementation of the **"Anything Everywhere"** node to streamline MODEL, CLIP, and VAE routing, reducing visual clutter and improving workflow maintainability.
* **Intelligent Compositing:** Uses a dual-masking system to isolate the print zone from the garment body, allowing for independent control over shirt color and design placement.

## 🛠️ Workflow Architecture

The workflow is divided into six logical processing groups:

1.  **Models:** Loads the Flux Fill stack (UNET, Dual CLIP, VAE) optimized for inpainting tasks.
2.  **Load Image:** Dual-path loading for the T-shirt mockup and the specific design/logo.
3.  **Custom Node (Color Swap):** Executes the precise transformation of the shirt's base color using the `ShirtColorSwapper`.
4.  **Image Processing:** Handles resizing, bounding box calculations, and mask compositing to align the print perfectly on the garment.
5.  **Generation:** The core KSampler loop utilizing `InpaintModelConditioning` and `FluxGuidance` (set to 3.5) for stable, photorealistic results.
6.  **Save Image:** Automated file naming and organization (stored in `/Shirt/`) for rapid batch production.

## ⏱️ Performance & Efficiency

By automating the masking and texture integration, this workflow transforms the traditional post-production timeline:
* **Conventional Method:** 15–30 minutes per variant (Manual masking and Displacement Maps in Photoshop).
* **AI Pipeline:** < 1 minute per automated variant.
* **Result:** **90%+ time reduction** in creating full seasonal color palettes for e-commerce stores.

## 📖 Installation & Usage

1.  **Requirements:** Ensure you have the `flux1-fill-dev` models and the `ComfyUI_essentials` suite installed.
2.  **Custom Nodes:** You will need the `rgthree`, `kjnodes`, and the specific `ShirtColorSwapper` node integrated into your custom_nodes folder.
3.  **Setup:** Drop the `.json` file into ComfyUI, upload your white T-shirt mockup, and enter your desired Hex color and design prompt.

---
*Optimized for professional E-Commerce environments and Print-on-Demand (POD) scalability.*
