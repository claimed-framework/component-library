cwlVersion: v1.2
class: CommandLineTool

baseCommand: "claimed"

inputs:
  component:
    type: string
    default: docker.io/mdorzweiler/claimed-input-xview-clipping:0.1
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
  window_size:
    type: string
    default: None
    inputBinding:
      position: 4
      prefix: --window_size
  step_size:
    type: string
    default: None
    inputBinding:
      position: 5
      prefix: --step_size


outputs: []