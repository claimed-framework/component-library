cwlVersion: v1.2
class: CommandLineTool

baseCommand: "claimed"

inputs:
  component:
    type: string
    default: docker.io/mdorzweiler/claimed-image-tiling:0.1
    inputBinding:
      position: 1
      prefix: --component
  log_level:
    type: string
    default: "INFO"
    inputBinding:
      position: 2
      prefix: --log_level
  directory_path:
    type: string
    default: None
    inputBinding:
      position: 3
      prefix: --directory_path
  destination:
    type: string
    default: None
    inputBinding:
      position: 4
      prefix: --destination
  tile_size_x:
    type: string
    default: None
    inputBinding:
      position: 5
      prefix: --tile_size_x
  tile_size_y:
    type: string
    default: None
    inputBinding:
      position: 6
      prefix: --tile_size_y
  stride_x:
    type: string
    default: None
    inputBinding:
      position: 7
      prefix: --stride_x
  stride_y:
    type: string
    default: None
    inputBinding:
      position: 8
      prefix: --stride_y


outputs: []
