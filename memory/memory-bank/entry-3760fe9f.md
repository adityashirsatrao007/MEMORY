---
created: 2026-08-17T10:08:20.400348
category: ml-engineering
tags: ["tensorflow", "gpu", "cuda", "cudnn", "troubleshooting", "tf-gpu"]
---

TensorFlow 2.19 GPU fix (GTX 1650 Ti, CUDA driver 595.84): "Cannot dlopen some GPU libraries" was caused by version mismatch nvidia-cusolver-cu12 11.7.5.82 needing cublasSetEnvironmentMode (cuBLAS>=12.8) vs nvidia-cublas-cu12 12.5.3.2 pinned by TF 2.19. Fix: downgrade cusolver-cu12 to 11.6.1.9. Also TF resolves GPU libs via ldconfig NOT LD_LIBRARY_PATH, so pip-installed nvidia libs must be registered: wrote /etc/ld.so.conf.d/tf-venv-cu12.conf with venv nvidia/*/lib dirs + sudo ldconfig. venv at /home/aditya/venv. Verify with tf.config.list_physical_devices('GPU').
