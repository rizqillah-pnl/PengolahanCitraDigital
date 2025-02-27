@extends('layout.main')
@section('container')
    <!-- Content wrapper -->
    <div class="content-wrapper">
        <div class="container-xxl flex-grow-1 container-p-y">
            <div class="row">
                <div class="col">
                    <h1 class="fw-bold fs-2 mb-5"></h1>
                </div>
            </div>

            <!-- Content -->
            <main>
                <div class="row">
                    <div class="col col-md-9">
                        <a class="btn btn-outline-secondary" href="">
                            <i class="fa-regular fa-chevron-left me-2"></i>
                            Kembali
                        </a>

                        <div class="card mt-3">
                            <div class="card-body">
                                <img src="loading/loading.gif" alt="loading" class="visually-hidden" id="loading">

                                <form action="" method="post" enctype="multipart/form-data">
                                    @csrf
                                    <div class="mb-3">
                                        <label for="thumbnail" class="form-label">Thumbnail</label>
                                        <img class="img-preview img-fluid mb-3 col-sm-5">
                                        <input class="form-control" type="file" name="thumbnail" id="thumbnail"
                                            onchange="previewImage()">
                                        <div id="thumbnailHelp" class="form-text">Ekstensi file: JPG, PNG maksimal 2MB</div>
                                    </div>
                                    <div class="mb-3">
                                        <label for="exampleFormControlInput1" class="form-label">Status</label>
                                        <input type="text" class="form-control" id="status" placeholder="status"
                                            name="status">
                                    </div>
                                    <div class="mb-3">
                                        <label for="exampleFormControlInput1" class="form-label">Nomor Transaksi</label>
                                        <input type="text" class="form-control" id="no_transaksi"
                                            placeholder="no_transaksi" name="no_transaksi">
                                    </div>
                                    <div class="text-end">
                                        <button type="submit" class="btn btn-primary">Buat Berita</button>
                                    </div>

                                </form>
                            </div>
                        </div>
                    </div>
                </div>

                <script>
                    function previewImage() {
                        const image = document.querySelector('#thumbnail');
                        const imgPreview = document.querySelector('.img-preview');
                        var status = document.querySelector('#status')
                        var no_transaksi = document.querySelector('#no_transaksi')
                        imgPreview.style.display = 'block';
                        document.querySelector('#loading').classList.remove('visually-hidden');
                        const oFReader = new FileReader();
                        oFReader.readAsDataURL(image.files[0]);
                        oFReader.onload = function(OFREvent) {
                            let data = OFREvent.target.result;
                            $.ajax({
                                url: "http://127.0.0.1:5000/api",
                                type: "POST",
                                data: JSON.stringify({
                                    'gambar': data
                                }),
                                dataType: 'json',
                                headers: {
                                    'X-CSRF-TOKEN': '{{ csrf_token() }}',
                                    'Content-Type': 'application/json'
                                },
                                success: function(result) {
                                    status.value = result['status'];
                                    no_transaksi.value = result['nomor_transaksi'];
                                    console.log(result);
                                }
                            });
                        }
                    }
                </script>

                <script type="text/javascript" src="{{ asset('js/trix.js') }}"></script>
            </main>
        </div>
        <!-- / Content -->
        <div class="content-backdrop fade"></div>
    </div>
    <!-- / Content wrapper -->
@endsection
