from django import forms
from django.conf import settings

from main.models import Experience, Project

ACCESS_CODE_NOT_CONFIGURED = "Kode akses belum dikonfigurasi di server."
ACCESS_CODE_WRONG = "Kode akses salah."


def access_code_error(supplied_code):
    """Balikin pesan error kalau kode akses tidak valid, atau None kalau valid.

    Dipakai dua tempat: field password di form tulis (Project/Experience), dan
    tombol hapus di dalam modal konfirmasi (main/views.py). Selama
    PORTFOLIO_ACCESS_CODE kosong, semua request tulis ditolak.
    """
    expected_code = settings.PORTFOLIO_ACCESS_CODE

    if not expected_code:
        return ACCESS_CODE_NOT_CONFIGURED

    if supplied_code != expected_code:
        return ACCESS_CODE_WRONG

    return None


class AccessCodeFormMixin(forms.Form):
    """Field kode akses yang dipakai bareng oleh semua form tulis.

    Kodenya divalidasi di form (bukan cuma di view) supaya request yang
    langsung POST tanpa lewat browser juga ditolak.
    """

    access_code = forms.CharField(
        label="Kode Akses",
        required=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Kode rahasia portofolio"}
        ),
        help_text="Hanya pemilik portofolio yang tahu kode ini.",
    )

    def clean_access_code(self):
        supplied_code = self.cleaned_data.get("access_code", "")
        error = access_code_error(supplied_code)

        # Kode yang belum di-set di server harus kelihatan penyebabnya, bukan
        # tertutup pesan "field harus diisi".
        if error == ACCESS_CODE_NOT_CONFIGURED:
            raise forms.ValidationError(error)

        if not supplied_code:
            raise forms.ValidationError("Kode akses wajib diisi.")

        if error:
            raise forms.ValidationError(error)

        return supplied_code


class DateRangeFormMixin:
    """Validasi umum form ber-field tanggal: selesai tidak boleh < mulai."""

    def clean(self):
        cleaned_data = super().clean()
        started_at = cleaned_data.get("started_at")
        ended_at = cleaned_data.get("ended_at")
        if started_at and ended_at and ended_at < started_at:
            self.add_error(
                "ended_at", "Tanggal selesai tidak boleh lebih awal dari tanggal mulai."
            )
        return cleaned_data


class ProjectForm(AccessCodeFormMixin, DateRangeFormMixin, forms.ModelForm):
    """Form tambah proyek, dibangun otomatis dari model Project."""

    class Meta:
        model = Project
        fields = [
            "title",
            "category",
            "description",
            "technologies",
            "repository_url",
            "report_url",
            "deployment_url",
            "started_at",
            "ended_at",
        ]
        labels = {
            "title": "Nama Proyek",
            "category": "Kategori",
            "description": "Deskripsi Proyek",
            "technologies": "Teknologi yang Digunakan",
            "repository_url": "URL Repositori",
            "report_url": "URL Laporan",
            "deployment_url": "URL Demo",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Website Portofolio PBP", "maxlength": 255}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Ceritakan proyeknya", "rows": 4}
            ),
            "technologies": forms.TextInput(
                attrs={"placeholder": "Django, HTML5, CSS3"}
            ),
            "repository_url": forms.URLInput(
                attrs={"placeholder": "https://github.com/fikrioktos/myportofolio"}
            ),
            "report_url": forms.URLInput(
                attrs={"placeholder": "https://drive.google.com/file/d/..."}
            ),
            "deployment_url": forms.URLInput(
                attrs={"placeholder": "https://contoh-demo.com"}
            ),
            "started_at": forms.DateInput(attrs={"type": "date"}),
            "ended_at": forms.DateInput(attrs={"type": "date"}),
        }


class ExperienceForm(AccessCodeFormMixin, DateRangeFormMixin, forms.ModelForm):
    """Form tambah pengalaman, dibangun otomatis dari model Experience."""

    class Meta:
        model = Experience
        fields = [
            "title",
            "role",
            "organization",
            "description",
            "category",
            "thumbnail",
            "organization_url",
            "started_at",
            "ended_at",
        ]
        labels = {
            "title": "Posisi/Judul",
            "role": "Peran",
            "organization": "Organisasi",
            "description": "Deskripsi Kegiatan",
            "category": "Kategori",
            "thumbnail": "URL Gambar (opsional)",
            "organization_url": "Situs Organisasi (opsional)",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Asisten Dosen PBP", "maxlength": 255}
            ),
            "role": forms.TextInput(
                attrs={"placeholder": "Asisten Dosen", "maxlength": 255}
            ),
            "organization": forms.TextInput(
                attrs={"placeholder": "Fakultas Ilmu Komputer UI", "maxlength": 255}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Ceritakan kegiatannya", "rows": 4}
            ),
            "thumbnail": forms.URLInput(
                attrs={"placeholder": "https://contoh.com/foto.png"}
            ),
            "organization_url": forms.URLInput(
                attrs={"placeholder": "https://cs.ui.ac.id"}
            ),
            "started_at": forms.DateInput(attrs={"type": "date"}),
            "ended_at": forms.DateInput(attrs={"type": "date"}),
        }
