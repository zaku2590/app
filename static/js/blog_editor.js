const quill = new Quill('#editor', {
  theme: 'snow',
  placeholder: '本文をここに入力...',
  modules: {
    toolbar: {
      container: [
        [{ header: [1, 2, 3, false] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ 'color': [] }, { 'background': [] }],
        [{ list: 'ordered' }, { list: 'bullet' }],
        ['link', 'image'],
        ['clean']
      ],
      handlers: {
        image: imageHandler
      }
    }
  }
});

function imageHandler() {
  const input = document.createElement('input');
  input.setAttribute('type', 'file');
  input.setAttribute('accept', 'image/*');
  input.click();

  input.onchange = () => {
    const file = input.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('image', file);

    fetch('/upload_image', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(result => {
      if (result.success) {
        const range = quill.getSelection();
        quill.insertEmbed(range.index, 'image', result.file.url);
      } else {
        alert("アップロードに失敗しました：" + result.error);
      }
    });
  };
}

// base64貼り付け無効化
quill.clipboard.addMatcher('IMG', function(node, delta) {
  const src = node.getAttribute('src');
  if (src && src.startsWith('data:image')) {
    alert('画像はアップロードして使用してください（ペーストは非対応です）');
    return new Delta();
  }
  return delta;
});

// 本文を hidden input に保存
const form = document.querySelector('form');
form.addEventListener('submit', function () {
  const contentInput = document.querySelector('input[name=content]');
  contentInput.value = quill.root.innerHTML;
});