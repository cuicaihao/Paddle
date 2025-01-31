#   Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import paddle


class TestAdagradOpV2(unittest.TestCase):
    def test_v20_coverage(self):
        paddle.disable_static()
        inp = paddle.rand(shape=[10, 10])
        linear = paddle.nn.Linear(10, 10)
        out = linear(inp)
        loss = paddle.mean(out)
        adagrad = paddle.optimizer.Adagrad(
            learning_rate=0.1, parameters=linear.parameters()
        )
        out.backward()
        adagrad.step()
        adagrad.clear_grad()


class TestAdagradOpV2Group(TestAdagradOpV2):
    def test_v20_coverage(self):
        paddle.disable_static()
        inp = paddle.rand(shape=[10, 10])
        linear_1 = paddle.nn.Linear(10, 10)
        linear_2 = paddle.nn.Linear(10, 10)
        out = linear_1(inp)
        out = linear_2(out)
        loss = paddle.mean(out)
        adagrad = paddle.optimizer.Adagrad(
            learning_rate=0.01,
            parameters=[
                {'params': linear_1.parameters()},
                {
                    'params': linear_2.parameters(),
                    'weight_decay': 0.001,
                },
            ],
            weight_decay=0.1,
        )
        out.backward()
        adagrad.step()
        adagrad.clear_grad()


if __name__ == "__main__":
    unittest.main()
