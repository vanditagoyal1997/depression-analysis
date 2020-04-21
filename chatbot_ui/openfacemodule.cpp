#include <Python.h>

static PyObject *trial(PyObject *self)
{
	printf("hi");
	Py_RETURN_NONE;

}

static PyMethodDef helloworld_funcs[] = {
   {"trial", (PyCFunction)trial, 
      METH_NOARGS, NULL},
      {NULL}
};

static struct PyModuleDef helloworld_module = {
    PyModuleDef_HEAD_INIT,
    "trial",
    NULL,
    -1,
    helloworld_funcs
};

PyMODINIT_FUNC PyInit_trial(void) {
    return PyModule_Create(&helloworld_module);
}


/*static PyObject *
conv_gaze_au(PyObject *self)
{
	LandmarkDetector::FaceModelParameters det_parameters;
LandmarkDetector::CLNF face_model(det_parameters.model_location);	

while(video)
{
    bool success = LandmarkDetector::DetectLandmarksInVideo(grayscale_image, face_model, det_parameters);
			
    cv::Point3f gazeDirection0(0, 0, -1);
    cv::Point3f gazeDirection1(0, 0, -1);
	cv::Vec2d gazeAngle(0, 0);

    if (success && det_parameters.track_gaze)
    {
        GazeAnalysis::EstimateGaze(face_model, gazeDirection0, fx, fy, cx, cy, true);
        GazeAnalysis::EstimateGaze(face_model, gazeDirection1, fx, fy, cx, cy, false);
		gazeAngle = GazeAnalysis::GetGazeAngle(gazeDirection0, gazeDirection1, pose_estimate);
    }
}
}*/