import os
from figma_export.figma import FigmaService
from .AbstractExporter import AbstractExporter


class ImageExporter(AbstractExporter):
    """Exports Figma document and saves the result to image files"""
    supported_formats = ["png", "jpg", "svg"]

    def __call__(
        self,
        scale: AbstractExporter.ScaleArgument,
        selector: AbstractExporter.SelectorArgument
    ):
        figma_service = FigmaService()
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print("Files in %r: %s" % (cwd, files))
        print("self.document_id")
        print(self.document_id)
        print("selector")
        print(selector)
        document = figma_service.load_document(self.document_id)
        if not os.path.isdir(document.name):
            os.mkdir(document.name)
        os.chdir(document.name)

        rendering_results = figma_service.render_components_n(
            document,
            self.export_format,
            scale,
            selector
        )
        # print(rendering_results)
        for result in rendering_results:
            if result.scale == 1:
                path = f"{result.node.id}.{result.format}"
            else:
                path = f"{result.node.name}_x{result.scale}.{result.format}"
            print("Saving.....")
            path = path.replace(' / ',"_")
            path = path.replace('/', "_")
            path = path.replace(' ', "_")
            print(path)
            with open(path, "wb") as f:
                f.write(result.data)
