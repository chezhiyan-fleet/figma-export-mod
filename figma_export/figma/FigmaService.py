import json
from typing import List
from .FigmaClient import FigmaClient
from .FigmaDocument import FigmaDocument
from .FigmaNode import FigmaNode
from .FigmaRenderingResult import FigmaRenderingResult


class FigmaService:
    def __init__(self):
        self.__client = FigmaClient()

    def load_document(
        self,
        document_id: str
    ):
        data = json.loads(
            self.__client.request_document_data(document_id)
        )

        current_path = []
        paths = {}
        print("document length")

        def find_components(current_data):
            # print(current_data)

            if current_data.get("type") == "COMPONENT" or current_data.get("type") == "RECTANGLE":
                print(current_data.get("name")," -> " ,current_data.get('id'), " -> /" + "/".join(current_path))
                paths[current_data.get('id')] = "/" + "/".join(current_path)
                return
            current_path.append(current_data.get("name"))
            for k, v in current_data.items():
                if isinstance(v, list) and k == "children":
                    for node in v:
                        find_components(node)
            current_path.pop()

        # Serializing json
        # json_object = json.dumps(data, indent=2)
        #
        # # Writing to sample.json
        # with open("sample.json", "w") as outfile:
        #     outfile.write(json_object)
        #
        find_components(data["document"])


        def get_fig_node(kv, paths_dict):
            print(kv)
            if kv[0] in paths_dict:
                return FigmaNode(
                    kv[0],
                    kv[1],
                    paths_dict[kv[0]])
            else:
                print(kv[0], kv[1]["name"])
                return None

        return FigmaDocument(
            document_id,
            data["name"],
            list(filter(None, list(
                map(
                    lambda kv: get_fig_node(kv, paths),
                    paths.items()
                )
            )))
        )

    def render_components(
            self,
            document: FigmaDocument,
            rendering_format: str,
            scale: float = 1,
            select_expression: str = None
    ) -> List[FigmaRenderingResult]:
        rendering_results = []
        if select_expression is None:
            components = document.components
        else:
            components = list(filter(
                lambda component:
                component.path.startswith(select_expression),
                document.components
            ))
        if len(components) == 0:
            return rendering_results
        image_urls = json.loads(
            self.__client.request_image_urls(
                document.id,
                list(map(lambda node: node.id, components)),
                scale,
                rendering_format)
        )
        for component in components:
            rendering_results.append(
                FigmaRenderingResult(
                    component,
                    rendering_format,
                    scale,
                    self.__client.request_data(image_urls["images"][component.id])
                )
            )
        return rendering_results

    def render_components_n(
            self,
            document: FigmaDocument,
            rendering_format: str,
            scale: float = 1,
            select_expression: str = None
    ) -> List[FigmaRenderingResult]:
        rendering_results = []


        if select_expression is None:
            components = document.components
        else:
            components = list(filter(
                lambda component:
                component.path.startswith(select_expression),
                document.components
            ))
        if len(components) == 0:
            return rendering_results
        image_urls = json.loads(
            self.__client.request_image_urls(
                document.id,
                list(map(lambda node: node.id, components)),
                scale,
                rendering_format)
        )
        print(image_urls)
        for component in components:
            indi_components_list = (component.id).split(",")
            for indi_component in indi_components_list:
                if not image_urls["images"][indi_component]:
                    continue
                rendering_results.append(
                    FigmaRenderingResult(
                        FigmaNode(indi_component, component.name, component.path),
                        rendering_format,
                        scale,
                        self.__client.request_data(image_urls["images"][indi_component])
                    )
                )

        return list(filter(None, rendering_results))