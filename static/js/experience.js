(() => {
    const config = window.experienceConfig;

    if (!config) {
        return;
    }

    const { endpoints, isSuperuser, isAuthenticated, canEdit } = config;
    const dummyUuid = "00000000-0000-0000-0000-000000000000";
    const searchDebounceDelay = 300;

    const loadingState = document.getElementById("experience-loading");
    const errorState = document.getElementById("experience-error");
    const emptyState = document.getElementById("experience-empty");
    const gridContainer = document.getElementById("experience-grid");
    const searchForm = document.getElementById("experience-search-form");
    const searchInput = document.getElementById("experience-search-input");
    const formModal = document.getElementById("experience-form-modal");
    const experienceForm = document.getElementById("experience-form");
    const formTitle = document.getElementById("experience-form-modal-title");
    const submitButton = document.getElementById("experience-form-submit");

    let searchDebounceTimer;
    let experiencesAbortController;
    // null = mode tambah (POST); berisi id = mode ubah (PATCH)
    let editingExperienceId = null;
    // Snapshot data dari API supaya modal ubah bisa diisi tanpa fetch ulang
    const experienceById = new Map();

    function displayPageSection({
        showLoading = false,
        showError = false,
        showEmpty = false,
        showGrid = false,
    }) {
        loadingState.classList.toggle("hide", !showLoading);
        errorState.classList.toggle("hide", !showError);
        emptyState.classList.toggle("hide", !showEmpty);
        gridContainer.classList.toggle("hide", !showGrid);
    }

    function escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#39;");
    }

    function getCookie(name) {
        const prefix = `${name}=`;
        const cookie = document.cookie
            .split(";")
            .map((value) => value.trim())
            .find((value) => value.startsWith(prefix));
        return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : null;
    }

    function endpointFor(template, experienceId) {
        return template.replace(dummyUuid, experienceId);
    }

    // Pesan error DRF: {"field": ["..."]} atau {"detail": "..."}
    function apiErrorMessage(data, status) {
        const messages = Object.values(data)
            .flat()
            .filter((value) => typeof value === "string");
        return messages.join(" ") || `Terjadi kesalahan (HTTP ${status}).`;
    }

    // Satu tempat untuk POST/PATCH/DELETE/star: JSON, CSRF, dan error konsisten
    async function writeExperience(url, method, payload) {
        const response = await fetch(url, {
            method,
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: payload === undefined ? undefined : JSON.stringify(payload),
        });

        if (response.status === 204) {
            return null;
        }

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(apiErrorMessage(data, response.status));
        }

        return data;
    }

    function buildStarButton(experience) {
        if (!isAuthenticated) {
            return `<a href="/login/" class="button" title="Login untuk memberi star">
                <span aria-hidden="true">★</span> Star
                <span class="star-count">${escapeHtml(experience.star_count)}</span>
            </a>`;
        }

        const isStarredClass = experience.is_starred ? " is-starred" : "";
        const starText = experience.is_starred ? "Unstar" : "Star";
        const starTitle = experience.star_count > 0
            ? `Dibintangi oleh ${escapeHtml(experience.starred_by_names)}`
            : "Jadilah yang pertama memberi star";

        return `
            <button type="button"
                    class="button button-star${isStarredClass}"
                    data-action="star"
                    data-id="${escapeHtml(experience.id)}"
                    title="${starTitle}">
                <span aria-hidden="true">★</span>
                ${starText}
                <span class="star-count">${escapeHtml(experience.star_count)}</span>
            </button>
        `;
    }

    function buildExperienceCardElement(experience) {
        const articleElement = document.createElement("article");
        const startYear = escapeHtml(experience.started_at).slice(0, 4);
        const period = experience.is_ongoing
            ? `${startYear} – Present`
            : `${startYear} – ${escapeHtml(experience.ended_at).slice(0, 4)}`;
        const organizationLink = experience.organization_url
            ? `<a href="${escapeHtml(experience.organization_url)}"
                  class="timeline-link"
                  target="_blank"
                  rel="noopener">Kunjungi situs</a>`
            : "";
        const updateHtml = canEdit
            ? `<button type="button" class="timeline-action-link" data-action="edit" data-id="${escapeHtml(experience.id)}">Ubah</button>`
            : "";
        const deleteHtml = isSuperuser
            ? `<button type="button" class="button button-danger experience-delete-button" data-action="delete" data-id="${escapeHtml(experience.id)}">Hapus</button>`
            : "";

        articleElement.className = "timeline-item";
        articleElement.innerHTML = `
            <div class="timeline-meta">
                <span class="timeline-period">${period}</span>
                <span class="timeline-role">${escapeHtml(experience.role)}</span>
            </div>

            <div class="timeline-content">
                <h3>${escapeHtml(experience.title)}</h3>

                ${experience.organization
                    ? `<p class="timeline-org">${escapeHtml(experience.organization)}</p>`
                    : ""}

                ${organizationLink}

                <ul>
                    <li>${escapeHtml(experience.description)}</li>
                </ul>

                <div class="timeline-actions">
                    ${buildStarButton(experience)}
                    ${updateHtml}
                    ${deleteHtml}
                </div>
            </div>
        `;

        return articleElement;
    }

    async function fetchExperiences(searchQuery = "") {
        if (experiencesAbortController) {
            experiencesAbortController.abort();
        }

        experiencesAbortController = new AbortController();

        try {
            displayPageSection({ showLoading: true });

            const url = new URL(endpoints.list, window.location.origin);
            if (searchQuery) {
                url.searchParams.set("title", searchQuery);
            }

            const response = await fetch(url, {
                headers: { Accept: "application/json" },
                signal: experiencesAbortController.signal,
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const experiences = await response.json();

            experienceById.clear();
            experiences.forEach((experience) => {
                experienceById.set(experience.id, experience);
            });

            gridContainer.replaceChildren(
                ...experiences.map(buildExperienceCardElement)
            );
            displayPageSection({
                showGrid: experiences.length > 0,
                showEmpty: experiences.length === 0,
            });
        } catch (error) {
            if (error.name === "AbortError") {
                return;
            }

            console.error("Error loading experiences:", error);
            displayPageSection({ showError: true });
        }
    }

    function openExperienceForm(experience = null) {
        editingExperienceId = experience ? experience.id : null;
        formTitle.textContent = experience
            ? "Ubah Experience"
            : "Tambah Experience Baru";
        submitButton.textContent = experience
            ? "Simpan Perubahan"
            : "Tambah Experience";

        experienceForm.reset();
        if (experience) {
            experienceForm.elements.title.value = experience.title;
            experienceForm.elements.role.value = experience.role;
            experienceForm.elements.organization.value = experience.organization;
            experienceForm.elements.description.value = experience.description;
            experienceForm.elements.category.value = experience.category;
            experienceForm.elements.thumbnail.value = experience.thumbnail || "";
            experienceForm.elements.organization_url.value = experience.organization_url || "";
            experienceForm.elements.started_at.value = experience.started_at;
            experienceForm.elements.ended_at.value = experience.ended_at || "";
        }

        formModal.showPopover();
    }

    // Field URL & tanggal kosong dikirim sebagai null, bukan string kosong
    function readExperiencePayload() {
        const fields = new FormData(experienceForm);
        const nullable = ["thumbnail", "organization_url", "ended_at"];

        return Object.fromEntries(
            [
                "title", "role", "organization", "description", "category",
                "thumbnail", "organization_url", "started_at", "ended_at",
            ].map((name) => {
                const value = fields.get(name);
                return [name, nullable.includes(name) && !value ? null : value];
            })
        );
    }

    async function saveExperience(event) {
        event.preventDefault();
        submitButton.disabled = true;

        const isEdit = editingExperienceId !== null;

        try {
            const payload = readExperiencePayload();

            if (isEdit) {
                await writeExperience(
                    endpointFor(endpoints.detailTemplate, editingExperienceId),
                    "PATCH",
                    payload
                );
            } else {
                await writeExperience(endpoints.list, "POST", payload);
            }

            formModal.hidePopover();
            showToast(
                "Berhasil",
                isEdit
                    ? "Experience berhasil diperbarui!"
                    : "Experience baru berhasil ditambahkan!",
                "success"
            );
            await fetchExperiences(searchInput.value.trim());
        } catch (error) {
            console.error("Error saving experience:", error);
            showToast(
                isEdit ? "Gagal memperbarui experience" : "Gagal menambahkan experience",
                error.message,
                "error"
            );
        } finally {
            submitButton.disabled = false;
        }
    }

    async function runCardAction(button) {
        const action = button.dataset.action;
        const experienceId = button.dataset.id;

        if (action === "edit") {
            openExperienceForm(experienceById.get(experienceId));
            return;
        }

        if (action === "delete" && !window.confirm("Yakin ingin menghapus experience ini?")) {
            return;
        }

        button.disabled = true;

        try {
            if (action === "star") {
                await writeExperience(
                    endpointFor(endpoints.starTemplate, experienceId),
                    "POST"
                );
            } else {
                await writeExperience(
                    endpointFor(endpoints.detailTemplate, experienceId),
                    "DELETE"
                );
            }

            const successMessage = action === "star"
                ? "Star diperbarui!"
                : "Experience berhasil dihapus!";
            showToast("Berhasil", successMessage, "success");
            await fetchExperiences(searchInput.value.trim());
        } catch (error) {
            console.error("Error:", error);
            showToast("Permintaan gagal", error.message, "error");
        } finally {
            button.disabled = false;
        }
    }

    function searchExperiences() {
        fetchExperiences(searchInput.value.trim());
    }

    searchInput.addEventListener("input", () => {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(searchExperiences, searchDebounceDelay);
    });

    searchForm.addEventListener("submit", (event) => {
        event.preventDefault();
        clearTimeout(searchDebounceTimer);
        searchExperiences();
    });

    // Event delegation: satu listener untuk semua tombol di kartu
    gridContainer.addEventListener("click", (event) => {
        const button = event.target.closest("button[data-action]");

        if (button && !button.disabled) {
            runCardAction(button);
        }
    });

    if (experienceForm) {
        experienceForm.addEventListener("submit", saveExperience);
    }

    const addButton = document.querySelector(".experience-add-button");
    if (addButton) {
        addButton.addEventListener("click", () => openExperienceForm(null));
    }

    fetchExperiences(searchInput.value.trim());
})();
