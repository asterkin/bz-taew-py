# Glossary

This glossary consolidates key terms used throughout the **CypherAI Verity Matcher** documentation to ensure consistent usage and understanding.

## General Terms

- **Administrator**: A role or entity responsible for managing the registration, updates, and overall administration of various endpoints (Verity Sources, Candidate Sources, Notification Targets). There are three types of administrators:
  - **Verity Source Administrator**: Manages Verity Sources.
  - **Candidate Source Administrator**: Manages Candidate Sources.
  - **Notification Target Administrator**: Manages Notification Targets.

- **Candidate**: A real-world object or entity to be verified or authenticated against a Verity. Examples include a person, artwork, product, or any other entity whose authenticity or identity is under evaluation.

- **Digital Encoding**: A digital representation of a real-world object, capturing its characteristics in various formats such as text, images, audio, or video. Digital encodings are used for analysis, comparison, or verification within the system.

- **Notification Target**: An entity or endpoint that receives the results of comparisons between Candidate Snapshots and Verity Snapshots. This could include auction houses, antiquity stores, or other stakeholders interested in being informed of comparison outcomes.

- **Real-World Object**: An actual entity or object in the physical world, such as a person, animal, work of art, product, or any other tangible item. Real-world objects are represented digitally within the system for purposes of analysis or verification.

## System-Specific Terms

- **Candidate Source**: An entity that submits Candidate Snapshots (digital encodings of real-world objects) to the system for evaluation against Verity Snapshots. This can include sources like students, sellers, or automated systems providing works or items to be verified.

- **Candidate Snapshot**: A digital encoding of a Candidate, created in various formats (text, images, video, etc.), used to determine whether it matches or corresponds to a Verity Snapshot.

- **Candidate Embedding**: A mathematical vector representation of a Candidate Snapshot, often derived using machine learning algorithms, for comparison against Verity Embeddings.

- **Candidate Embedding Evaluation Request**: A request to evaluate Candidate Embeddings against stored Verity Embeddings to determine similarity or match.

- **Candidate Embedding Distance**: A numerical measure representing the distance between a Candidate Embedding and a Verity Embedding, indicating the degree of similarity.

- **Candidate Distance Notification**: A message sent to a Notification Target containing the results of comparing Candidate Embeddings against Verity Embeddings, including relevant metadata and calculated distances.

- **Encrypted Candidate Embedding Distance**: A Candidate Embedding Distance that has been encrypted to ensure secure transmission and storage.

- **Verity**: An original real-world object or entity considered authentic or authoritative, such as a person, work of art, product, etc. Verities serve as benchmarks against which Candidates are compared for verification.

- **Verity Source**: An entity responsible for supplying Verity Snapshots (digital encodings of Verities) to the system. This could be an organization, individual, or database that provides digital representations of Verities for use as authoritative references.

- **Verity Snapshot**: A digital encoding of a Verity, captured in various formats (e.g., text, images, audio, or video). Verity Snapshots are used as authoritative references for comparison against Candidate Snapshots.

- **Verity Embedding**: A mathematical vector representation of a Verity Snapshot, often derived using machine learning algorithms, for comparison against Candidate Embeddings.

- **Verity Embeddings Encryption Request**: A request to encrypt Verity Embeddings for secure storage and transmission.

- **Encrypted Verity Embedding**: A Verity Embedding that has been encrypted to ensure secure transmission and storage.

- **Verity Snapshot Batch**: A collection of Verity Snapshots grouped together for processing, comparison, or analysis.

- **Verity Snapshot Batch Embeddings**: A set of Verity Embeddings corresponding to a Verity Snapshot Batch, used for comparison against Candidate Embeddings.

- **Encrypted Verity Batch Embeddings**: A set of encrypted Verity Embeddings derived from a Verity Snapshot Batch.

- **Verity Embedding Distance**: A numerical measure representing the distance between different Verity Embeddings, used to evaluate the diversity and information content of a Verity Batch.

## Technical Terms

- **Adapter**: A software component that interfaces between the core application and external systems (e.g., databases, messaging services). Adapters implement the specific protocols defined by ports in the core logic.

- **Component Plus Strategy**: An architectural approach used to encapsulate algorithmic variations or internal adapter implementations, allowing flexibility in choosing different algorithms or methods without modifying the core application.

- **Port**: An abstract interface that defines how the core application interacts with external systems or actors (e.g., ForVeritySource, ForEncryption). Ports represent the points of communication in the "Ports and Adapters" architecture.

- **Strategy**: A design pattern used to define a family of algorithms or methods, allowing the algorithms to be interchangeable based on the context.
