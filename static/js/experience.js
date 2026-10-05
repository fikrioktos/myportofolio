(() => {
    const config = window.experienceConfig;

    if (!config) {
        return;
    }

    const {
        endpoints,
        isSuperuser,
        canEdit,
    } = config;
    const dummyUuid = "00000000-0000-0000-0000-000000000000";
    const searchDebounceDelay = 300;

    const loadingState = document.getElementById("experience-loading");
    const errorState = document.getElementById("experience-error");
    const emptyState = document.getElementById("experience-empty");
    const gridContainer = document.getElementById("experience-grid");
    const searchForm = document.getElementById("experience-search-form");
    const searchInput = document.getElementById("experience-search-input");
    const experienceForm = document.getElementById("experience-form");

    let searchDebounceTimer;
    let experiencesAbortController;

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
        let cookieValue = null;

        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");

            for (let index = 0; index < cookies.length; index += 1) {
                const cookie = cookies[index].trim();

                if (cookie.substring(0, name.length + 1) === `${name}=`) {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }

        return cookieValue;
    }

    function getExperienceUrl(template, experienceId) {
        return template.replace(dummyUuid, experienceId);
    }

    function getStarTitle(starCount, starredByNames) {
        return starCount > 0
            ? `Dibintangi oleh ${escapeHtml(starredByNames)}`
            : "Jadilah yang pertama memberi star";
    }

    function buildStarButton(starUrl, experience) {
        const isStarredClass = experience.is_starred ? " is-starred" : "";
        const starText = experience.is_starred ? "Unstar" : "Star";
        const starTitle = getStarTitle(
            experience.star_count,
            experience.starred_by_names
        );

        return `
            <button type="button"
                    class="button button-star${isStarredClass}"
                    data-star-url="${escapeHtml(starUrl)}"
                    title="${starTitle}">
                <span aria-hidden="true">★</span>
                ${starText}
                <span class="star-count">${escapeHtml(experience.star_count)}</span>
            </button>
        `;
    }

    function buildExperienceCardElement(item) {
        const experience = item.fields;
        const experienceId = item.pk;
        const articleElement = document.createElement("article");
        const period = experience.is_ongoing
            ? `${escapeHtml(experience.started_at).slice(0, 4)} – Present`
            : `${escapeHtml(experience.started_at).slice(0, 4)} – ${escapeHtml(experience.ended_at).slice(0, 4)}`;
        const organizationLink = experience.organization_url
            ? `<a href="${escapeHtml(experience.organization_url)}"
                  class="timeline-link"
                  target="_blank"
                  rel="noopener">Kunjungi situs</a>`
            : "";
        const updateUrl = getExperienceUrl(
            endpoints.updateTemplate,
            experienceId
        );
        const deleteUrl = getExperienceUrl(
            endpoints.deleteTemplate,
            experienceId
        );
        const starUrl = getExperienceUrl(endpoints.starTemplate, experienceId);
        const updateHtml = canEdit
            ? `<a href="${escapeHtml(updateUrl)}" class="timeline-action-link">Ubah</a>`
            : "";
        const csrfToken = getCookie("csrftoken");
        const deleteHtml = isSuperuser
            ? `<form method="post" action="${escapeHtml(deleteUrl)}" class="delete-form">
                    <input type="hidden"
                           name="csrfmiddlewaretoken"
                           value="${escapeHtml(csrfToken)}">
                    <input type="password"
                           name="access_code"
                           placeholder="Kode akses"
                           required>
                    <button type="submit"
                            class="button button-danger experience-delete-button"
                            onclick="return confirm('Yakin ingin menghapus experience ini?');">
                        Hapus
                    </button>
                </form>`
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
                    ${buildStarButton(starUrl, experience)}
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

            const url = searchQuery
                ? `${endpoints.list}?title=${encodeURIComponent(searchQuery)}`
                : endpoints.list;
            const response = await fetch(url, {
                headers: { Accept: "application/json" },
                signal: experiencesAbortController.signal,
            });

            if (!response.ok) {
                throw new Error("Failed to fetch experience data");
            }

            const experienceData = await response.json();

            if (experienceData.length === 0) {
                displayPageSection({ showEmpty: true });
                return;
            }

            gridContainer.innerHTML = "";
            experienceData.forEach((item) => {
                gridContainer.appendChild(buildExperienceCardElement(item));
            });
            displayPageSection({ showGrid: true });
        } catch (error) {
            if (error.name === "AbortError") {
                return;
            }

            console.error("Error loading experiences:", error);
            displayPageSection({ showError: true });
        }
    }

    async function toggleExperienceStar(starButton) {
        starButton.disabled = true;

        try {
            const response = await fetch(starButton.dataset.starUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            });
            const result = await response.json().catch(() => ({}));

            if (!response.ok) {
                showToast(
                    "Tidak dapat memberi star",
                    result.message || "Silakan login terlebih dahulu.",
                    "error"
                );
                return;
            }

            const nextExperience = {
                is_starred: result.is_starred,
                star_count: result.star_count,
                starred_by_names: result.starred_by_names,
            };
            starButton.outerHTML = buildStarButton(
                starButton.dataset.starUrl,
                nextExperience
            );
        } catch (error) {
            console.error("Error toggling experience star:", error);
            showToast(
                "Tidak dapat memberi star",
                "Tidak dapat terhubung ke server. Silakan coba lagi.",
                "error"
            );
        } finally {
            starButton.disabled = false;
        }
    }

    function closeExperienceModal() {
        const modal = document.getElementById("add-experience-modal");

        if (modal) {
            modal.hidePopover();
        }
    }

    async function addExperience(event) {
        event.preventDefault();

        const submitButton = experienceForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        try {
            const response = await fetch(endpoints.create, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: new FormData(experienceForm),
            });
            const result = await response.json().catch(() => ({}));

            if (response.status === 201) {
                experienceForm.reset();
                closeExperienceModal();
                showToast(
                    "Berhasil",
                    "Experience baru berhasil ditambahkan!",
                    "success"
                );
                fetchExperiences(searchInput.value.trim());
                return;
            }

            const errorMessages = result.errors
                ? Object.values(result.errors)
                    .flat()
                    .map((error) => error.message)
                : [
                    result.message
                    || `Terjadi kesalahan (status ${response.status}).`,
                ];

            showToast(
                "Gagal menambahkan experience",
                errorMessages.join(" "),
                "error"
            );
        } catch (error) {
            console.error("Error adding experience:", error);
            showToast(
                "Gagal menambahkan experience",
                "Tidak dapat terhubung ke server. Silakan coba lagi.",
                "error"
            );
        } finally {
            submitButton.disabled = false;
        }
    }

    function searchExperiences() {
        fetchExperiences(searchInput.value.trim());
    }

    searchInput.addEventListener("input", () => {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(
            searchExperiences,
            searchDebounceDelay
        );
    });

    searchForm.addEventListener("submit", (event) => {
        event.preventDefault();
        clearTimeout(searchDebounceTimer);
        searchExperiences();
    });

    gridContainer.addEventListener("click", (event) => {
        const starButton = event.target.closest("[data-star-url]");

        if (starButton) {
            toggleExperienceStar(starButton);
        }
    });

    if (experienceForm) {
        experienceForm.addEventListener("submit", addExperience);
    }

    fetchExperiences(searchInput.value.trim());
})();
