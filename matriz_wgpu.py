import wgpu
import numpy as np
from numpy import pi

wsx = 3
wsy = 3

matriz = np.array([[1,2,3],[4,5,6],[7,8,9]],dtype=np.float32)

device = wgpu.utils.get_default_device()

with open('MATRIZES.wgsl') as shader_file:
    cshader_string = shader_file.read()
    cshader_string = cshader_string.replace('wsx', f'{wsx}')
    cshader_string = cshader_string.replace('wsy', f'{wsy}')
    cshader = device.create_shader_module(code=cshader_string)

buffer = device.create_buffer_with_data(data=matriz, usage=wgpu.BufferUsage.STORAGE |
                                                         wgpu.BufferUsage.COPY_DST |
                                                         wgpu.BufferUsage.COPY_SRC)

bl_mat = [
    {"binding": 0,
     "visibility": wgpu.ShaderStage.COMPUTE,
     "buffer": {
         "type": wgpu.BufferBindingType.storage}
     }
]

b_mat = [
    {
        "binding": 0,
        "resource": {"buffer": buffer, "offset": 0, "size": buffer.size},
    }
]

bgl_0 = device.create_bind_group_layout(entries=bl_mat)
pipeline_layout = device.create_pipeline_layout(bind_group_layouts=[bgl_0])
bg_0 = device.create_bind_group(layout=bgl_0, entries=b_mat)

compute_teste = device.create_compute_pipeline(layout=pipeline_layout,
                                                          compute={"module": cshader,
                                                                   "entry_point": "matriz_kernel"})

command_encoder = device.create_command_encoder()
compute_pass = command_encoder.begin_compute_pass()
compute_pass.set_bind_group(0, bg_0, [], 0, 999999)

# for i in range(wsx):
compute_pass.set_pipeline(compute_teste)
compute_pass.dispatch_workgroups(wsx,wsy)

compute_pass.end()
device.queue.submit([command_encoder.finish()])

out = np.array(device.queue.read_buffer(buffer).cast("f").tolist())
outmat= out.reshape(wsx,wsy)

print(outmat)

