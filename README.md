# FaceSwap-Toolkit-for-Realistic-AI-Avatars

> A modular and research-driven toolkit for face swapping and realistic face generation using ROOP, SimSwap, ReActor, E4S, and Pivotal Tuning Inversion (PTI).

---

## 🎯 Overview

This repository documents a comprehensive exploration of **face swapping between a source image and a target video**, with the goal of generating a **realistic, non-existent yet aesthetically pleasing identity** in video content.

📍 This work integrates multiple face-swapping frameworks and advanced face editing techniques, with emphasis on **realism, consistency**, and **pipeline modularity**.

---

## 🧠 Objectives

- 🔄 **Face Swapping:** Swap a source identity onto a target face in a video.
- 🧬 **Realistic Face Generation:** Construct a "mean" face using Pivotal Tuning Inversion (PTI) from celebrity datasets.
- 🎨 **Visual Enhancement:** Ensure smooth transitions, consistency, and visual realism across frames.

---

## 🛠️ Methods & Frameworks

| Tool       | Description |
|------------|-------------|
| **ROOP**   | Real-time one-shot face swapping, efficient for videos |
| **ReActor**| High-fidelity face swapping using deep learning |
| **SimSwap**| Simple and effective facial identity swapping |
| **E4S**    | All-in-one framework combining multiple swap techniques |
| **Mobile FaceSwap** | Lightweight, mobile-compatible solution |
| **DifFace**| Detail-aware face swap with improved fine feature handling |

---

## 🧪 Planned Methodology

### 🧬 Face Editing Pipeline (PTI-based)

| Step | Description |
|------|-------------|
| 1. Image Collection | Collect ~20 celebrity face images |
| 2. Mean Face Synthesis | Use PTI + GAN inversion to create a hybrid identity |
| 3. Video Integration | Use this synthesized identity as the source for face-swapping |

---

## 🔄 Project Files

```
.
├── 1_ReActor_UI.ipynb       # ReActor-based face swapping notebook
├── simswap.ipynb            # SimSwap face swap pipeline
├── boomerang.py             # Boomerang-style loop video generator
├── change_bg.py             # Background replacement for videos
├── video_repeat.py          # Frame repetition for output stabilization
├── resize.py                # Input video resizing tool
├── pti_vgg_solvetheproblem  # Face editing (PTI troubleshooting module)
├── *.whl                    # CUDA/torch environment wheels
└── README.md
```

---

## 💻 Development Environment

- **OS:** Ubuntu
- **IDE:** VSCode
- **CUDA:** 11.3
- **Torch:** 1.13.1+cu113
- **Python:** 3.8+

Precompiled wheels included:
- `torchvision-0.13.1+cu113`
- `torchaudio-0.12.1+cu113`

---

## 🔍 Evaluation Criteria

- 🎭 **Realism:** Visual believability of the swapped identity
- 🔄 **Consistency:** Temporal coherence across video frames
- 🌟 **Aesthetics:** Visual appeal of generated identities

---

## 🔗 References

- ROOP: [GitHub](https://github.com/s0md3v/roop)
- ReActor
- SimSwap: _SimSwap: An Efficient Framework For High Fidelity Face Swapping_
- E4S
- Mobile FaceSwap
- DifFace

---

## 📜 License

This repository is for **research and educational purposes only**.  
Use of face-swapping technology should comply with ethical standards and local laws.

---

## 🧾 Papers (To Be Added)

- [ ] ROOP
- [ ] ReActor
- [ ] SimSwap
- [ ] DifFace
- [ ] Mobile FaceSwap
- [ ] Pivotal Tuning Inversion (PTI)

---

## 📌 Notes

> This work was conducted during personal research & internship settings.  
> The project aims to explore the intersection of **generative AI**, **face manipulation**, and **identity synthesis** in video.

